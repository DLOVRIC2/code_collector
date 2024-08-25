import os
import fnmatch

import logging


class Node:
    def __init__(self, name, is_dir=False, parent=None):
        self.name = name
        self.is_dir = is_dir
        self.children = []
        self.selected = False
        self.expanded = True
        self.parent = parent


logging.basicConfig(level=logging.DEBUG, format="%(message)s")


class CodeCollector:
    def __init__(self, config):
        self.config = config
        self.root = None
        self.cursor_node = None
        self.all_nodes = []
        self.ignore_patterns = self.load_ccignore()
        logging.debug(f"Loaded ignore patterns: {self.ignore_patterns}")

    def load_ccignore(self):
        ignore_file = os.path.join(self.config["directory"], ".ccignore")
        patterns = [
            ".git",
            "__pycache__",
            "*.egg-info",
            ".pytest_cache",
            ".vscode",
            ".idea",
        ]
        if os.path.exists(ignore_file):
            with open(ignore_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        return patterns

    def should_ignore(self, path):
        rel_path = os.path.relpath(path, self.config["directory"])
        name = os.path.basename(path)

        for pattern in self.ignore_patterns:
            # Check for exact matches (e.g., .git, __pycache__)
            if fnmatch.fnmatch(name, pattern):
                logging.debug(f"Ignoring {rel_path} (exact match: {pattern})")
                return True

            # Check for directory matches (e.g., .venv, test_dir)
            if os.path.isdir(path) and fnmatch.fnmatch(name, pattern):
                logging.debug(f"Ignoring {rel_path} (directory match: {pattern})")
                return True

            # Check for path part matches (e.g., */.git/*)
            if any(fnmatch.fnmatch(part, pattern) for part in rel_path.split(os.sep)):
                logging.debug(f"Ignoring {rel_path} (path part match: {pattern})")
                return True

            # Check for file extension patterns (e.g., *.pyc)
            if pattern.startswith("*") and name.endswith(pattern[1:]):
                logging.debug(f"Ignoring {rel_path} (extension match: {pattern})")
                return True

            # Check for nested patterns (e.g., **/*.egg-info)
            if "**" in pattern and fnmatch.fnmatch(rel_path, pattern):
                logging.debug(f"Ignoring {rel_path} (nested pattern match: {pattern})")
                return True

        logging.debug(f"Not ignoring {rel_path}")
        return False

    def run(self):
        if self.config["interactive"]:
            self.interactive_mode()
        else:
            self.collect_files()

    def interactive_mode(self):
        self.root = self.build_tree(self.config["directory"])
        self.cursor_node = self.all_nodes[0]
        self.display_tree()

        while True:
            key = self.get_key()
            if key == "q":
                print("Quitting without processing selection.")
                return
            elif key == "f":
                break
            elif key in ["up", "k"]:
                self.move_cursor(-1)
            elif key in ["down", "j"]:
                self.move_cursor(1)
            elif key == "space":
                self.toggle_expand()
            elif key == "enter":
                self.toggle_select()

            self.display_tree()

        selected_files = self.get_selected_files(self.root)
        self.aggregate_files(selected_files)

    def build_tree(self, path, parent=None):
        logging.debug(f"Building tree for: {path}")
        if self.should_ignore(path):
            logging.debug(f"Ignoring path: {path}")
            return None

        name = os.path.basename(path) or path
        node = Node(name, is_dir=os.path.isdir(path), parent=parent)
        self.all_nodes.append(node)

        if node.is_dir:
            try:
                for item in sorted(os.listdir(path)):
                    item_path = os.path.join(path, item)
                    if self.should_ignore(item_path):
                        logging.debug(f"Ignoring item: {item_path}")
                        continue
                    if os.path.isdir(item_path) or self.config["interactive"]:
                        child = self.build_tree(item_path, parent=node)
                        if child:
                            node.children.append(child)
                    elif any(item.endswith(ext) for ext in self.config["file_types"]):
                        child = self.build_tree(item_path, parent=node)
                        if child:
                            node.children.append(child)
            except PermissionError:
                logging.error(f"Permission denied: {path}")
        return node

    def display_tree(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("CodeCollector Interactive Mode")
        print("------------------------------")
        print(
            "↑/k ↓/j: Navigate  Space: Expand/Collapse  Enter: Select  f: Finish  q: Quit"
        )
        print("------------------------------")
        self._display_node(self.root, "")

    def _display_node(self, node, prefix):
        marker = ">" if node == self.cursor_node else " "
        checkbox = "[x]" if node.selected else "[ ]"
        expander = (
            "- " if node.is_dir and node.expanded else "+ " if node.is_dir else "  "
        )
        print(f"{prefix}{marker}{checkbox}{expander}{node.name}")

        if node.is_dir and node.expanded:
            for i, child in enumerate(node.children):
                is_last = i == len(node.children) - 1
                new_prefix = prefix + ("    " if is_last else "│   ")
                self._display_node(child, new_prefix)

    def get_key(self):
        import termios, fcntl, sys, os

        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
        try:
            while True:
                try:
                    c = sys.stdin.read(1)
                    if c == "\x1b":
                        c2 = sys.stdin.read(1)
                        c3 = sys.stdin.read(1)
                        if c2 == "[":
                            if c3 == "A":
                                return "up"
                            elif c3 == "B":
                                return "down"
                    elif c == " ":
                        return "space"
                    elif c == "\n":
                        return "enter"
                    elif c in ["k", "j", "q", "f"]:
                        return c
                except IOError:
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    def move_cursor(self, direction):
        current_index = self.all_nodes.index(self.cursor_node)
        new_index = current_index
        while True:
            new_index = (new_index + direction) % len(self.all_nodes)
            new_node = self.all_nodes[new_index]
            if new_node == self.root or self.is_node_visible(new_node):
                break
        self.cursor_node = self.all_nodes[new_index]

    def is_node_visible(self, node):
        current = node.parent
        while current != self.root:
            if not current.expanded:
                return False
            current = current.parent
        return True

    def toggle_expand(self):
        if self.cursor_node.is_dir:
            self.cursor_node.expanded = not self.cursor_node.expanded

    def toggle_select(self):
        self.cursor_node.selected = not self.cursor_node.selected
        if self.cursor_node.is_dir:
            self._toggle_children(self.cursor_node)

    def _toggle_children(self, node):
        for child in node.children:
            child.selected = node.selected
            if child.is_dir:
                self._toggle_children(child)

    def get_selected_files(self, node):
        files = []
        if node.selected:
            if node.is_dir:
                files.extend(self._get_all_files(node))
            else:
                files.append(self._get_full_path(node))
        elif node.is_dir:
            for child in node.children:
                files.extend(self.get_selected_files(child))
        return files

    def _get_all_files(self, node):
        files = []
        for child in node.children:
            if child.is_dir:
                files.extend(self._get_all_files(child))
            else:
                files.append(self._get_full_path(child))
        return files

    def _get_full_path(self, node):
        path = []
        current = node
        while current != self.root:
            path.append(current.name)
            current = current.parent
        path.append(self.config["directory"])
        return os.path.join(*reversed(path))

    def collect_files(self):
        base_dir = self.config["directory"]
        files = self.collect_files_from_dir(base_dir)
        self.aggregate_files(files)

    def collect_files_from_dir(self, directory):
        files = []
        for root, _, filenames in os.walk(directory):
            if self.should_ignore(root):
                continue
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if not self.should_ignore(file_path) and any(
                    filename.endswith(ext) for ext in self.config["file_types"]
                ):
                    files.append(file_path)
            if not self.config["recursive"]:
                break
        return files

    def aggregate_files(self, files):
        output_file = self.config["output"]
        with open(output_file, "w") as out:
            for file_path in files:
                out.write(f"// File: {file_path}\n\n")
                try:
                    with open(file_path, "r") as f:
                        out.write(f.read())
                except Exception as e:
                    out.write(f"Error reading file: {str(e)}\n")
                out.write("\n\n")

        print(f"Aggregated {len(files)} files into {output_file}")

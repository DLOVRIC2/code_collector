# CodeCollector

CodeCollector is a powerful CLI tool designed to help developers easily aggregate and organize code files from complex projects, specifically tailored for providing context to Large Language Models (LLMs) in development workflows.

<div align="center">
  <img src="./files/codecollector.gif" alt="CodeCollector in action" width="1200"/>
</div>

## Purpose

When working on large, complex projects, it can be challenging to provide comprehensive context to LLMs about your codebase. Manually copying and pasting relevant files from various parts of your project is time-consuming and error-prone. CodeCollector solves this problem by allowing you to easily select and aggregate the most relevant code files, creating a consolidated view of your project that can be readily shared with an LLM for more accurate and context-aware assistance.

## Features

- Aggregate code files from specified directories
- Interactive mode for selecting specific files and directories
- Customizable file type filtering
- Recursive directory traversal
- Ignore patterns support (similar to .gitignore)
- Configuration file support
- Optimized for providing context to LLMs

## Installation

You can install CodeCollector using pip:

```
pip install codecollector
```

## Usage

### Basic Usage

To run CodeCollector in its default mode:

```
codecollector
```

This will start the interactive mode in the current directory, allowing you to select the files you want to include in your LLM context.

### Command-line Options

```
codecollector [OPTIONS]
```

Options:
- `-d, --directory TEXT`: Base directory to start searching from (default: current directory)
- `-o, --output TEXT`: Output file name (default: aggregated_output.txt)
- `-r, --recursive / --no-recursive`: Enable/disable recursive search (default: recursive)
- `-t, --file-types TEXT`: File types to include (can be used multiple times, default: .py)
- `-i, --interactive`: Launch interactive mode (default: False in CLI, True when run without arguments)
- `--version`: Show the version and exit
- `--help`: Show this message and exit

### Examples

1. Interaactive mode starting from current dir

   ```
   codecollector -i
   ```

   You should then be able to navigate through the project tree and select files whose content you want to include.

   ![Interactive mode of codecollector](/files/codecollector.png)


2. Collect Python files recursively from the current directory for LLM context:
   ```
   codecollector
   ```

3. Collect JavaScript and TypeScript files from a specific project for LLM analysis:
   ```
   codecollector -d /path/to/project -t .js -t .ts
   ```

4. Non-recursive collection of Ruby files with a custom output name for focused LLM input:
   ```
   codecollector --no-recursive -t .rb -o ruby_context.txt
   ```

5. Interactive mode starting from a specific directory to selectively choose files for LLM context:
   ```
   codecollector -i -d /path/to/project
   ```

### Interactive Mode

In interactive mode, use the following keys to select the most relevant files for your LLM context:
- ↑/k: Move cursor up
- ↓/j: Move cursor down
- Space: Expand/Collapse directory
- Enter: Select/Deselect file or directory
- f: Finish selection and process files
- q: Quit without processing

### Configuration File

You can create a `codecollector.yaml` file in your project root to set default options:

```yaml
directory: /path/to/project
output: llm_context.txt
recursive: true
file_types:
  - .py
  - .js
  - .ts
interactive: true
```

### Ignore Patterns

Create a `.ccignore` file in your project root to specify ignore patterns:

```
**/.git/**
**/__pycache__/**
**/*.egg-info/**
**/.pytest_cache/**
**/.vscode/**
**/.idea/**
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape CodeCollector
- Inspired by the need for better context provision to LLMs in complex development projects
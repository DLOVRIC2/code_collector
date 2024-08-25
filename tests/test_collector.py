import os
import pytest
from codecollector.collector import CodeCollector, Node


@pytest.fixture
def mock_config():
    return {
        "directory": "/test/dir",
        "output": "test_output.txt",
        "recursive": True,
        "file_types": [".py", ".js"],
        "interactive": False,
    }


@pytest.fixture
def collector(mock_config):
    return CodeCollector(mock_config)


def test_load_ccignore(tmp_path, collector):
    ccignore_content = """
    *.pyc
    .venv
    # This is a comment
    test_dir
    """
    ccignore_file = tmp_path / ".ccignore"
    with open(ccignore_file, "w") as f:
        f.write(ccignore_content)

    collector.config["directory"] = str(tmp_path)
    patterns = collector.load_ccignore()

    assert ".git" in patterns
    assert "*.pyc" in patterns
    assert ".venv" in patterns
    assert "test_dir" in patterns
    assert "# This is a comment" not in patterns


def test_build_tree(tmp_path, collector):
    # Create a mock directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.py").touch()
    (tmp_path / "dir1" / "file2.js").touch()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "file3.py").touch()
    (tmp_path / ".git").mkdir()

    collector.config["directory"] = str(tmp_path)
    root = collector.build_tree(str(tmp_path))

    assert root.name == tmp_path.name
    assert len(root.children) == 2  # dir1 and dir2, .git should be ignored
    assert {child.name for child in root.children} == {"dir1", "dir2"}

    dir1 = next(child for child in root.children if child.name == "dir1")
    assert len(dir1.children) == 2
    assert {child.name for child in dir1.children} == {"file1.py", "file2.js"}


def test_collect_files(tmp_path, collector):
    # Create a mock directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.py").touch()
    (tmp_path / "dir1" / "file2.js").touch()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "file3.py").touch()
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").touch()
    (tmp_path / "ignored_file.pyc").touch()

    collector.config["directory"] = str(tmp_path)
    files = collector.collect_files_from_dir(str(tmp_path))

    assert len(files) == 3
    assert set(files) == {
        str(tmp_path / "dir1" / "file1.py"),
        str(tmp_path / "dir1" / "file2.js"),
        str(tmp_path / "dir2" / "file3.py"),
    }
    assert str(tmp_path / "ignored_file.pyc") not in files
    assert str(tmp_path / ".git" / "config") not in files

import os
import yaml
import pytest
from codecollector.config import load_config


@pytest.fixture
def mock_config_file(tmp_path):
    config_content = {
        "directory": "/test/dir",
        "output": "test_output.txt",
        "recursive": True,
        "file_types": [".py", ".js"],
        "interactive": False,
    }
    config_file = tmp_path / "codecollector.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_content, f)
    return config_file


def test_load_config_with_file(mock_config_file, monkeypatch):
    monkeypatch.chdir(mock_config_file.parent)
    config = load_config()
    assert config == {
        "directory": "/test/dir",
        "output": "test_output.txt",
        "recursive": True,
        "file_types": [".py", ".js"],
        "interactive": False,
    }


def test_load_config_without_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config = load_config()
    assert config == {}

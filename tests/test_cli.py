import pytest
from click.testing import CliRunner
from codecollector.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def test_main_help(runner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output


def test_main_version(runner):
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_main_default_options(runner, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert "Aggregated" in result.output
    assert "aggregated_output.txt" in result.output

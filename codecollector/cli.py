import click
from .collector import CodeCollector
from .config import load_config


@click.command()
@click.option(
    "-d", "--directory", default=".", help="Base directory to start searching from."
)
@click.option(
    "-o", "--output", default="aggregated_output.txt", help="Output file name."
)
@click.option(
    "-r",
    "--recursive/--no-recursive",
    default=True,
    help="Enable/disable recursive search.",
)
@click.option(
    "-t", "--file-types", default=[".py"], multiple=True, help="File types to include."
)
@click.option("-i", "--interactive", is_flag=True, help="Launch interactive mode.")
@click.version_option(version="0.1.0")
def main(directory, output, recursive, file_types, interactive):
    """CodeCollector: Aggregate and organize code files from complex projects."""
    config = load_config()

    # Override config with command-line options
    config["directory"] = directory or config.get("directory", ".")
    config["output"] = output or config.get("output", "aggregated_output.txt")
    config["recursive"] = recursive
    config["file_types"] = file_types or config.get("file_types", [".py"])
    config["interactive"] = interactive or config.get("interactive", False)

    collector = CodeCollector(config)
    collector.run()


if __name__ == "__main__":
    main()

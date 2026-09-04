"""CLI template — replace with your actual commands."""

import click


@click.group()
def main() -> None:
    """Desenrolai CLI template."""


@main.command()
@click.option("--name", default="World", show_default=True, help="Name to greet.")
def hello(name: str) -> None:
    """Prints a greeting message."""
    click.echo(f"Hello, {name}! This is the Desenrolai CLI template.")


if __name__ == "__main__":
    main()

"""tg-cli — Telegram CLI entry point."""

import logging

import click

from .data import data_group
from .query import query_group
from .tg import tg_group


def _setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )


@click.group()
@click.version_option(package_name="tg-cli")
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging")
def cli(verbose: bool):
    """tg — Telegram CLI for monitoring chats, searching messages, and AI analysis."""
    _setup_logging(verbose)


# Register sub-groups
cli.add_command(tg_group, "tg")

# Register top-level query commands
for name, cmd in query_group.commands.items():
    cli.add_command(cmd, name)

# Register top-level data commands
for name, cmd in data_group.commands.items():
    cli.add_command(cmd, name)

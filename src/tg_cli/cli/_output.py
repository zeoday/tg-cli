"""Shared structured output helpers for CLI commands."""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Callable
from typing import Any

import click
import yaml

_OUTPUT_ENV = "OUTPUT"


def default_structured_format(*, as_json: bool, as_yaml: bool) -> str | None:
    """Resolve explicit flags first, then fall back to env and TTY defaults."""
    if as_json and as_yaml:
        raise click.UsageError("Use only one of --json or --yaml.")
    if as_yaml:
        return "yaml"
    if as_json:
        return "json"
    output_mode = os.getenv(_OUTPUT_ENV, "auto").strip().lower()
    if output_mode == "yaml":
        return "yaml"
    if output_mode == "json":
        return "json"
    if output_mode == "rich":
        return None
    if not sys.stdout.isatty():
        return "yaml"
    return None


def structured_output_options(command: Callable) -> Callable:
    """Add --json/--yaml flags to a click command."""
    command = click.option("--yaml", "as_yaml", is_flag=True, help="Output as YAML")(command)
    command = click.option("--json", "as_json", is_flag=True, help="Output as JSON")(command)
    return command


def emit_structured(data: Any, *, as_json: bool, as_yaml: bool) -> bool:
    """Emit structured output and return True when a structured format was used."""
    fmt = default_structured_format(as_json=as_json, as_yaml=as_yaml)
    if fmt is None:
        return False
    click.echo(dump_structured(data, fmt=fmt))
    return True


def dump_structured(data: Any, *, fmt: str) -> str:
    """Serialize structured data to JSON or YAML text."""
    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2, default=str)
    if fmt == "yaml":
        return yaml.safe_dump(
            data,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )
    raise ValueError(f"Unsupported structured format: {fmt}")

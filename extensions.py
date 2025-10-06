from __future__ import annotations

import re
import subprocess
import textwrap
import unicodedata
from datetime import date
from typing import Any

from jinja2.environment import Environment
from jinja2.ext import Extension


def git_user_name(default: str) -> str:
    return subprocess.getoutput("git config user.name").strip() or default


def git_user_email(default: str) -> str:
    return subprocess.getoutput("git config user.email").strip() or default


def slugify(value: Any, separator: str = "-"):
    value = (
        unicodedata.normalize("NFKD", str(value))
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-_\s]+", separator, value).strip("-_")


def wrap_text(text: str, width: int = 80) -> str:
    """Wrap text to specified width, preserving existing line breaks."""
    if not text:
        return text

    # Split by existing line breaks and wrap each paragraph
    paragraphs = text.split("\n")
    wrapped_paragraphs = []

    for paragraph in paragraphs:
        if paragraph.strip():
            wrapped = textwrap.fill(paragraph.strip(), width=width)
            wrapped_paragraphs.append(wrapped)
        else:
            wrapped_paragraphs.append("")

    return "\n".join(wrapped_paragraphs)


def ensure_period(text: str) -> str:
    """Ensure text ends with exactly one period."""
    if not text:
        return text

    text = text.strip()
    # Remove any trailing punctuation
    while text and text[-1] in ".!?":
        text = text[:-1]

    # Add exactly one period
    return text + "."


class MyExtensions(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)
        environment.filters["git_user_name"] = git_user_name
        environment.filters["git_user_email"] = git_user_email
        environment.filters["slugify"] = slugify
        environment.filters["wrap_text"] = wrap_text
        environment.filters["ensure_period"] = ensure_period
        environment.globals["current_year"] = date.today().year

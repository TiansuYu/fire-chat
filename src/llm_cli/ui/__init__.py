from prompt_toolkit.styles import Style as PromptStyle

from llm_cli.ui.console import console, ConsoleStyle
from llm_cli.ui.key_binding import create_keybindings

PROMPT_STYLE = PromptStyle([("", "fg:#AAFF00")])  # bright green

__all__ = ["console", "create_keybindings", "PROMPT_STYLE", "ConsoleStyle"]

from prompt_toolkit.styles import Style as PromptStyle

from fire_chat.ui.console import console, ConsoleStyle
from fire_chat.ui.key_binding import create_keybindings

PROMPT_STYLE = PromptStyle([("", "fg:#AAFF00")])  # bright green

__all__ = ["console", "create_keybindings", "PROMPT_STYLE", "ConsoleStyle"]

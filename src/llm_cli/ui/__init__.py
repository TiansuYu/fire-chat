from prompt_toolkit.styles import Style as PromptStyle
from rich.spinner import Spinner

from llm_cli.ui.console import console, ConsoleStyle
from llm_cli.ui.key_binding import create_keybindings

PROMPT_STYLE = PromptStyle([("", "fg:#AAFF00")])  # bright green


def get_spinner(text: str, name: str = "bouncingBar") -> Spinner:
    # see demo of all 'name's of spinners: https://www.youtube.com/watch?v=CLkLvOmNOjc
    return Spinner(name=name, text=text, style=ConsoleStyle.bold_yellow)


__all__ = ["console", "create_keybindings", "PROMPT_STYLE", "ConsoleStyle", "get_spinner"]

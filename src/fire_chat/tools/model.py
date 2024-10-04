from typing import Annotated

from litellm import model_list
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from pydantic import AfterValidator

from fire_chat.ui import console, ConsoleStyle


def validate_model(model: str) -> str:
    """If model not in LLMLite model list, prompt users to input a model."""
    session = PromptSession(key_bindings=KeyBindings())
    updated = False
    while model not in model_list:
        console.print(
            f"Invalid model '{model}'!",
            style=ConsoleStyle.bold_red,
        )
        model = session.prompt("Enter model: ", completer=WordCompleter(model_list))
    if updated:
        console.print(f"Model '{model}' successfully updated!.", style=ConsoleStyle.bold_green)
    return model


Model = Annotated[str, AfterValidator(validate_model)]

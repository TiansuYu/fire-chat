from litellm import provider_list
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from typing_extensions import Self

from pydantic import BaseModel, field_validator

from fire_chat.constants import DEFAULT_PROVIDER
from fire_chat.ui import console, ConsoleStyle


class Provider(BaseModel, validate_default=True, validate_assignment=True):
    api_key: str = "dummy api key"
    name: str = DEFAULT_PROVIDER
    proxy_url: str | None = None

    def merge(self, other: Self) -> Self:
        if self.name != other.name:
            return self
        return Provider(
            api_key=other.api_key or self.api_key,
            name=self.name,
            proxy_url=other.proxy_url or self.proxy_url,
        )

    @field_validator("name")
    def validate_provider(cls, name: str) -> str:
        session = PromptSession(key_bindings=KeyBindings())
        updated = False
        while name not in provider_list:
            console.print(
                f"Invalid provider '{name}'!.",
                style=ConsoleStyle.bold_red,
            )
            name = session.prompt("Enter provider: ", completer=WordCompleter(provider_list))
            updated = True
        if updated:
            console.print(f"Provider '{name}' successfully updated!.", style=ConsoleStyle.bold_green)
        return name

    def __str__(self):
        res = self.model_dump(exlude_none=True)  # noqa
        res["api_key"] = "*" * 8
        return res

    def __repr__(self):
        return f'Provider(name={self.name}, proxy_url={self.proxy_url}, api_key="********")'

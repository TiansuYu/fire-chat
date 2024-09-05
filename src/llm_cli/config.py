from dataclasses import field

from litellm import model_list, provider_list
from omegaconf import DictConfig, OmegaConf
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from pydantic import ConfigDict
from pydantic import field_validator, AfterValidator
from pydantic.dataclasses import dataclass
from typing_extensions import Annotated
from typing_extensions import Self

from llm_cli.budget import Budget
from llm_cli.constants import CONFIG_FILE, DEFAULT_MODEL
from llm_cli.str_enum import StrEnum
from llm_cli.ui import console
from llm_cli.ui.console import ConsoleStyle

__all__ = ["Config", "Provider", "StorageFormat", "Model"]


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


class StorageFormat(StrEnum):
    markdown = "markdown"
    json = "json"


@dataclass(config=ConfigDict(validate_default=True))
class Provider:
    api_key: str = field(default="dummy api key")
    name: str = field(default="openai")
    proxy_url: str | None = field(default=None)

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


@dataclass
class HistoryConf:
    save: str | bool = field(
        default=False,
        metadata={
            "description": "A file name or True. If a file name, will save history under HISTORY_DIR under that file name. "
                           "If True, will generate a new file name based on current timestamp."
                           "If False, history will be disabled."
        },
    )
    load_from: str | None = field(
        default=None, metadata={"description": "A file name under HISTORY_DIR to load history from."}
    )


@dataclass
class Config:
    providers: list[Provider] = field(default_factory=lambda: [Provider()])
    model: Model = field(default=DEFAULT_MODEL)
    temperature: float = 0.2
    markdown: bool = True
    easy_copy: bool = True
    json_mode: bool = False
    use_proxy: bool = False
    multiline: bool = False
    storage_format: StorageFormat = StorageFormat.markdown
    embedding_model: str = "text-embedding-ada-002"
    embedding_dimension: int = 1536
    max_context_tokens: int | None = None
    show_spinner: bool = True
    max_tokens: int | None = None
    budget: Budget = field(default_factory=Budget)
    history: HistoryConf = field(default_factory=HistoryConf)

    @property
    def suitable_provider(self) -> Provider:
        if self.model.startswith("gpt"):
            return _filter_provider_by_name(self.providers, "openai")
        if self.model.startswith("claude"):
            return _filter_provider_by_name(self.providers, "anthropic")
        raise NotImplementedError(f"Model '{self.model}' not supported")

    def add_or_update_provider(self, provider: Provider) -> None:
        self.providers = _add_or_update_provider(self.providers, provider)

    @classmethod
    def from_omega_conf(cls, cfg: DictConfig) -> Self:
        return OmegaConf.to_object(cfg)

    def get_api_key(self) -> str:
        return self.suitable_provider.api_key

    def save(self) -> None:
        self.budget.save()
        OmegaConf.save(self, CONFIG_FILE)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            console.print(f"An error occurred: {exc_val}", style=ConsoleStyle.bold_red)
        try:
            self.save()
        except Exception as e:
            console.print(f"An error occurred: {e}", style=ConsoleStyle.bold_red)


def _add_or_update_provider(existing_providers: list[Provider], provider: Provider):
    if provider.name not in [p.name for p in existing_providers]:
        return existing_providers + [provider]
    return [p.merge(provider) for p in existing_providers]


def _filter_provider_by_name(providers: list[Provider], name: str):
    for p in providers:
        if p.name == name:
            return p
    raise ValueError(f"No provider found with name '{name}'")

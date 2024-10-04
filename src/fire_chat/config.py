from __future__ import annotations

from dataclasses import field

import litellm
import yaml
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from pydantic import BaseModel
from typing_extensions import Self

from fire_chat.constants import (
    CONFIG_FILE,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_HISTORY_STORAGE_FORMAT,
    HistoryStorageFormat,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_EMBEDDING_DIMENSION,
    DEFAULT_MAX_TOKENS,
    DEFAULT_SHOW_SPINNER,
    DEFAULT_MULTILINE,
)
from fire_chat.tools.budget import Budget
from fire_chat.tools.model import Model
from fire_chat.tools.provider import Provider
from fire_chat.ui import console, ConsoleStyle


class HistoryConf(BaseModel):
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
    storage_format: HistoryStorageFormat = DEFAULT_HISTORY_STORAGE_FORMAT


class Config(BaseModel, validate_assignment=True):
    providers: list[Provider] = [Provider()]

    # chat
    model: Model = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    storage_format: HistoryStorageFormat = DEFAULT_HISTORY_STORAGE_FORMAT
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    embedding_dimension: int = DEFAULT_EMBEDDING_DIMENSION
    max_tokens: int = DEFAULT_MAX_TOKENS

    # ui
    show_spinner: bool = DEFAULT_SHOW_SPINNER
    multiline: bool = DEFAULT_MULTILINE
    use_markdown: bool = True

    # budgeting
    budget: Budget = Budget()

    # history
    history: HistoryConf = HistoryConf()

    @property
    def suitable_provider(self) -> Provider:
        if self.model.startswith("gpt"):
            return _filter_provider_by_name(self.providers, "openai")
        if self.model.startswith("claude"):
            return _filter_provider_by_name(self.providers, "anthropic")
        raise NotImplementedError(f"Model '{self.model}' not supported")

    def add_or_update_provider(self, provider: Provider) -> None:
        self.providers = _add_or_update_provider(self.providers, provider)

    def get_suitable_api_key(self) -> str:
        return self.suitable_provider.api_key

    def update_suitable_api_key(self, api_key: str) -> None:
        self.suitable_provider.api_key = api_key

    def validate_api_key(self):
        session = PromptSession(key_bindings=KeyBindings())
        updated = False
        while not litellm.check_valid_key(self.model, self.get_suitable_api_key()):
            console.print(
                f"Invalid API key '{_mask_key(self.get_suitable_api_key())}'!",
                style=ConsoleStyle.bold_red,
            )
            self.update_suitable_api_key(session.prompt("Enter API key: "))
            updated = True
        if updated:
            console.print(
                f"API key for '{self.suitable_provider.name}' successfully updated: "
                f"'{_mask_key(self.get_suitable_api_key())}'!.",
                style=ConsoleStyle.bold_green,
            )

    @classmethod
    def load(cls) -> Self:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                config = yaml.safe_load(f.read())
                return cls.model_validate(config)
        return Config()

    def save(self):
        parent_dir = CONFIG_FILE.parent
        if not parent_dir.exists():
            parent_dir.mkdir(parents=True)
        with open(CONFIG_FILE, "w+") as f:
            f.write(yaml.dump(self.model_dump(exclude_none=True)))
        if self.budget.is_on:
            self.budget.save()


def _add_or_update_provider(existing_providers: list[Provider], provider: Provider):
    if provider.name not in [p.name for p in existing_providers]:
        return existing_providers + [provider]
    return [p.merge(provider) for p in existing_providers]


def _filter_provider_by_name(providers: list[Provider], name: str):
    for p in providers:
        if p.name == name:
            return p
    raise ValueError(f"No provider found with name '{name}'")


def _mask_key(key: str) -> str:
    """
    If the key length is less than or equal to 6, mask the entire key.
    Otherwise, mask all characters except the first 3 and last 3.
    """
    if len(key) <= 6:
        return "*" * len(key)
    return key[:3] + "*" * (len(key) - 6) + key[-3:]

import json
import logging
from datetime import datetime

import fsspec
from pydantic import Field, BaseModel
from typing_extensions import Self

from fire_chat.config import Model
from fire_chat.constants import CONFIG_DIR
from fire_chat.message import Messages
from fire_chat.ui import ConsoleStyle, console

HISTORY_DIR = CONFIG_DIR / "session_history"

logger = logging.getLogger(__name__)


class History(BaseModel, validate_default=True):
    model: Model
    messages: Messages = Messages()
    timestamp: datetime = Field(default_factory=datetime.now)

    def save(self, file_name: str | None = None) -> None:
        try:
            file_name = file_name or _create_new_history_file_name()
            file_path = HISTORY_DIR / file_name
            with fsspec.open(file_path, "w+") as f:
                f.write(self.model_dump_json())
            console.print(f"History saved to {file_path}.", style=ConsoleStyle.bold_green)
        except Exception as e:
            console.print(f"Failed to save history: {e}", style=ConsoleStyle.bold_red)

    @classmethod
    def load(cls, file_name: str | None = None) -> Self | None:
        try:
            if not file_name:
                return None
            with fsspec.open(HISTORY_DIR / file_name, "r") as f:
                return History.model_validate(json.load(f))
        except Exception as e:
            console.print(f"Failed to load history: {e}", style=ConsoleStyle.bold_red)
            return None


def _get_current_timestamp_formatted() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")


def _create_new_history_file_name() -> str:
    return f"history-{_get_current_timestamp_formatted()}.json"

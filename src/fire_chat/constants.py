import logging
from pathlib import Path
from typing import Literal

from yaml import Dumper

PROJECT_NAME = "fire-chat"

CONFIG_DIR = Path.home() / ".config" / PROJECT_NAME
CONFIG_FILE = CONFIG_DIR / "config.yaml"

if not CONFIG_DIR.exists():
    CONFIG_DIR.mkdir(parents=True)

LOGGING_LEVEL = logging.ERROR

loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
for logger in loggers:
    logger.setLevel(LOGGING_LEVEL)

HistoryStorageFormat = Literal["json", "markdown"]

DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_HISTORY_STORAGE_FORMAT = "json"
DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
DEFAULT_EMBEDDING_DIMENSION = 1536
DEFAULT_SHOW_SPINNER = True
DEFAULT_MULTILINE = False
DEFAULT_USE_MARKDOWN = True
DEFAULT_MAX_TOKENS = 4096


class CustomYamlDumper(Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)

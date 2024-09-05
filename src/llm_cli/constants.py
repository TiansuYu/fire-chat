import logging
from pathlib import Path

PROJECT_NAME = "llm-cli"

CONFIG_DIR = Path.home() / ".config" / "llm-cli"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
DEFAULT_MODEL = "gpt-4o"

if not CONFIG_DIR.exists():
    CONFIG_DIR.mkdir(parents=True)

LOGGING_LEVEL = logging.ERROR

loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
for logger in loggers:
    logger.setLevel(LOGGING_LEVEL)

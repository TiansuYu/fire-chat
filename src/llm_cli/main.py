import warnings

import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding.key_bindings import key_binding
from rich.text import Text

from llm_cli.chat import LLMChat
from llm_cli.config import Config
from llm_cli.constants import CONFIG_FILE
from llm_cli.history import History
from llm_cli.message import Messages
from llm_cli.ui import PROMPT_STYLE, console, ConsoleStyle, create_keybindings

warnings.filterwarnings("ignore", category=UserWarning)

store = ConfigStore.instance()
store.store(name="config", node=Config)


def process_prompt(chat: LLMChat, prompt: str, index: int) -> None:
    """Process the prompt."""
    console.rule()
    result = chat.completion(prompt)
    console.print(Text(f"assistant [{index}]: ", style=ConsoleStyle.bold_blue), result, style=ConsoleStyle.blue)
    console.print("")


def print_header(config: Config):
    console.print()
    console.print(Text("Welcome to ChatGPT CLI!", style=ConsoleStyle.bold_yellow))
    console.print(Text(f"Provider: {config.suitable_provider.name}", style=ConsoleStyle.bold_yellow))
    console.print(Text(f"Model: {config.model}", style=ConsoleStyle.bold_yellow))
    console.print()


def bootstrap_config_file():
    """Bootstrap a config file if it does not exist."""
    if not CONFIG_FILE.exists():
        Config().save()


bootstrap_config_file()


# TODO: use typer instead of hydra
@hydra.main(
    version_base="1.3",
    config_path=str(CONFIG_FILE.parent),
    config_name=CONFIG_FILE.stem,
)
def main(cfg: DictConfig) -> None:
    with Config.from_omega_conf(cfg) as config:
        try:
            session = PromptSession(key_bindings=create_keybindings(config.multiline))
            print_header(config)
            chat = LLMChat(config=config, history=History.load(config.history.load_from))
            index = 1
            while True:
                prompt = session.prompt(f"user [{index}]: ", style=PROMPT_STYLE)
                process_prompt(chat, prompt, index)
                index += 1
        except KeyboardInterrupt:
            console.print()
            console.print("Goodbye!", style=ConsoleStyle.bold_green)
        finally:
            if config.budget.is_on:
                config.budget.display_expense()
            if save := config.history.save:
                save_to = None if isinstance(save, bool) else save
                chat.history.save(save_to)


if __name__ == "__main__":
    main()

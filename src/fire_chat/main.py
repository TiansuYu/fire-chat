import warnings
from typing import Annotated

import typer
from prompt_toolkit import PromptSession
from rich.text import Text

from fire_chat.chat import LLMChat
from fire_chat.config import Config, Provider, HistoryConf
from fire_chat.tools.history import History
from fire_chat.ui import console, ConsoleStyle
from fire_chat.ui import create_keybindings, PROMPT_STYLE

warnings.filterwarnings("ignore", category=UserWarning)

app = typer.Typer()

SPINNER = "bouncingBar"


def process_prompt(chat: LLMChat, prompt: str, index: int, *, use_markdown: bool, use_spinner: bool) -> None:
    """Process the prompt."""
    console.rule()
    if use_spinner:
        with console.status("Waiting for LLM response...", spinner=SPINNER):
            result = chat.completion(prompt, use_markdown)
    else:
        result = chat.completion(prompt, use_markdown)
    console.print(Text(f"assistant [{index}]: ", style=ConsoleStyle.bold_blue), result, style=ConsoleStyle.blue)
    console.print("")


def print_header(config: Config):
    console.print()
    console.print(Text("Welcome to ChatGPT CLI!", style=ConsoleStyle.bold_yellow))
    console.print(Text(f"Provider: {config.suitable_provider.name}", style=ConsoleStyle.bold_yellow))
    console.print(Text(f"Model: {config.model}", style=ConsoleStyle.bold_yellow))
    console.print()


def save_history_if_apply(chat: LLMChat, history_conf: HistoryConf):
    if save := history_conf.save:
        save_to = None if isinstance(save, bool) else save
        chat.history.save(save_to)


@app.command()
def main(
    # provider configs
    provider: Annotated[str | None, typer.Option(help="Providers to use")] = None,
    provider_api_key: Annotated[str | None, typer.Option(help="The API key for the provider to use")] = None,
    provider_proxy_url: Annotated[str | None, typer.Option(help="The proxy URL for the provider to use")] = None,
    # model configs
    model: Annotated[str | None, typer.Option(help="Model to use")] = None,
    temperature: Annotated[float | None, typer.Option(help="Model temperature")] = None,
    embedding_model: Annotated[str | None, typer.Option(help="Embedding model")] = None,
    embedding_dimension: Annotated[int | None, typer.Option(help="Embedding dimension")] = None,
    max_tokens: Annotated[int | None, typer.Option(help="Max tokens")] = None,
    # ui configs
    show_spinner: Annotated[bool | None, typer.Option(help="Show spinner")] = None,
    multiline: Annotated[bool | None, typer.Option(help="If accepts multilines in prompt input")] = None,
    use_markdown: Annotated[bool | None, typer.Option(help="If use markdown format in console output")] = None,
    # budget configs
    budget_enabled: Annotated[bool | None, typer.Option(help="Enable budget")] = None,
    budget_duration: Annotated[str | None, typer.Option(help="Budget duration")] = None,
    budget_amount: Annotated[float | None, typer.Option(help="Budget amount")] = None,
    budget_user: Annotated[str | None, typer.Option(help="Budget user")] = None,
    # history configs
    storage_format: Annotated[str | None, typer.Option(help="Storage format")] = None,
    load_history_from: Annotated[str | None, typer.Option(help="Load history from")] = None,
    save_history: Annotated[str | None, typer.Option(help="Save history")] = None,
) -> None:
    # loading configs from config file
    config = Config.load()

    # update configs according to CLI options
    if provider is not None:
        config.add_or_update_provider(Provider(name=provider, api_key=provider_api_key, proxy_url=provider_proxy_url))
    if model is not None:
        config.model = model
    if temperature is not None:
        config.temperature = temperature
    if embedding_model is not None:
        config.embedding_model = embedding_model
    if embedding_dimension is not None:
        config.embedding_dimension = embedding_dimension
    if max_tokens is not None:
        config.max_tokens = max_tokens
    if show_spinner is not None:
        config.show_spinner = show_spinner
    if multiline is not None:
        config.multiline = multiline
    if use_markdown is not None:
        config.use_markdown = use_markdown
    if budget_enabled:
        config.budget.enabled = True
        if budget_user is not None:
            config.budget.user = budget_user
        if budget_duration is not None:
            config.budget.duration = budget_duration
        if budget_amount is not None:
            config.budget.amount = budget_amount
    if storage_format is not None:
        config.history.storage_format = storage_format
    if load_history_from is not None:
        config.history.load_from = load_history_from
    if save_history is not None:
        config.history.save = save_history

    config.validate_api_key()

    # start prompt session
    session = PromptSession(key_bindings=create_keybindings(config.multiline))
    print_header(config)
    chat = LLMChat(config=config, history=History.load(config.history.load_from))
    try:
        index = 1
        while True:
            prompt = session.prompt(f"user [{index}]: ", style=PROMPT_STYLE)
            process_prompt(chat, prompt, index, use_markdown=config.use_markdown, use_spinner=config.show_spinner)
            index += 1
    except KeyboardInterrupt:
        console.print()
        console.print("Goodbye!", style=ConsoleStyle.bold_green)
    except:  # noqa: E722
        console.print_exception(show_locals=False, max_frames=10)
    finally:
        config.save()
        save_history_if_apply(chat, config.history)


if __name__ == "__main__":
    app()

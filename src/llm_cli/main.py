import warnings
from typing import Annotated

import typer
from rich.text import Text
from typer_config import use_yaml_config
from typer_config.decorators import dump_yaml_config

from llm_cli.budget import Budget
from llm_cli.chat import LLMChat
from llm_cli.config import Config, Provider, DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_STORAGE_FORMAT, \
    DEFAULT_EMBEDDING_MODEL, DEFAULT_EMBEDDING_DIMENSION, HistoryConf, StorageFormat
from llm_cli.constants import CONFIG_FILE
from llm_cli.ui import console, ConsoleStyle

warnings.filterwarnings("ignore", category=UserWarning)

app = typer.Typer()

SPINNER = "bouncingBar"


def process_prompt(chat: LLMChat, prompt: str, index: int, use_markdown: bool, use_spinner: bool) -> None:
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


@app.command()
@use_yaml_config(default_value=str(CONFIG_FILE))
@dump_yaml_config(str(CONFIG_FILE))
def main(
        providers: Annotated[
            list[Provider], typer.Option(help="Providers to use")] = [Provider()],
        model: Annotated[str, typer.Option(help="Model to use")] = DEFAULT_MODEL,
        temperature: Annotated[float, typer.Option(help="Model temperature")] = DEFAULT_TEMPERATURE,
        storage_format: Annotated[StorageFormat, typer.Option(help="Storage format")] = DEFAULT_STORAGE_FORMAT,
        embedding_model: Annotated[str, typer.Option(help="Embedding model")] = DEFAULT_EMBEDDING_MODEL,
        embedding_dimension: Annotated[int, typer.Option(help="Embedding dimension")] = DEFAULT_EMBEDDING_DIMENSION,
        show_spinner: Annotated[bool, typer.Option(help="Show spinner")] = True,
        multiline: Annotated[bool, typer.Option(help="If accepts multilines in prompt input")] = False,
        use_markdown: Annotated[bool, typer.Option(help="If use markdown format in console output")] = True,
        max_tokens: Annotated[int, typer.Option(help="Max tokens")] = 10 ** 9,
        budget: Annotated[Budget, typer.Option(help="Budget configuration")] = Budget(),
        history: Annotated[HistoryConf, typer.Option(help="History configuration")] = HistoryConf(),
) -> None:
    config = Config(
        providers=providers,
        model=model,
        temperature=temperature,
        storage_format=storage_format,
        embedding_model=embedding_model,
        embedding_dimension=embedding_dimension,
        show_spinner=show_spinner,
        multiline=multiline,
        use_markdown=use_markdown,
        max_tokens=max_tokens,
        budget=budget,
        history=history
    )
    typer.echo(config.model_dump())
    # session = PromptSession(key_bindings=create_keybindings(multiline))
    # print_header(config)
    # chat = LLMChat(config=config, history=History.load(config.history.load_from))
    # try:
    #     index = 1
    #     while True:
    #         prompt = session.prompt(f"user [{index}]: ", style=PROMPT_STYLE)
    #         process_prompt(chat, prompt, index, use_markdown, show_spinner)
    #         index += 1
    # except KeyboardInterrupt:
    #     console.print()
    #     console.print("Goodbye!", style=ConsoleStyle.bold_green)
    # finally:
    #     if config.budget.is_on:
    #         config.budget.display_expense()
    #         config.budget.save()
    #     if save := config.history.save:
    #         save_to = None if isinstance(save, bool) else save
    #         chat.history.save(save_to)


if __name__ == "__main__":
    app()

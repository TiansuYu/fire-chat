# LLM CLI

## Overview

This project provides a command-line interface (CLI) for interacting with various large language models (LLMs) using the
LiteLLM wrapper. It supports multiple providers, including OpenAI, Anthropic, Azure, and Gemini. The CLI allows users to
chat with these models, manage budgets, and handle API keys efficiently.

## Configuration

The configuration is managed through a `$HOME/.config/llm-cli/config.yaml` file. The first time you run the CLI run.
You can copy paste the starting config file [config.yaml](examples/config.yaml) to the location, adds your API key,
and quick start the application `llm-cli`.

## Installation and Usage

1. **Install the CLI**:

    ```shell
    pip install --user llm-cli # or pipx install llm-cli # requires python 3.10+
    ```

2. **Configure the CLI**:

   Edit the `$HOME/.config/llm-cli/config.yaml` file to set your preferred provider, model, and other settings.

3. **Run the CLI**:

    ```shell
    llm-cli
    ```

   or run with arguments (overriding config yaml file)

    ```shell
    llm-cli --model=gpt-4o
   ```

   for full list of configs, see [main.py](src/llm_cli/main.py).

4. **Exit**:
   To exit the CLI, `Ctrl+C`.

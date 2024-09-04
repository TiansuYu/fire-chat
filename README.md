# LLM CLI

## Overview

This project provides a command-line interface (CLI) for interacting with various large language models (LLMs) using the
LiteLLM wrapper. It supports multiple providers, including OpenAI, Anthropic, Azure, and Gemini. The CLI allows users to
chat with these models, manage budgets, and handle API keys efficiently.

## Configuration

The configuration is managed through a `$HOME/.config/llm-cli/config.yaml` file. The first time you run the CLI run, it
will generate this with default values for you (given that you have provided a correct model, provider and API key).

```yaml
providers:
  - api_key: abc # change to your key
    name: openai
  - api_key: abc # change to your key
    name: anthropic
model: claude-3-5-sonnet-20240620
temperature: 0.1
markdown: true
easy_copy: true
json_mode: false
use_proxy: false
multiline: false
storage_format: markdown
embedding_model: text-embedding-ada-002
embedding_dimension: 1536
show_spinner: true
```

## Installation and Usage

Only in testing phase, not published yet!

1. **Install the CLI**:

    ```shell
    uv install
    ```

2. **Configure the CLI**:

   Edit the `$HOME/.config/llm-cli/config.yaml` file to set your preferred provider, model, and other settings.

3. **Run the CLI**:

    ```shell
    uv run src/llm_cli/main.py
    ```

   or run with arguments (overriding config yaml file)

    ```shell
    uv run src/llm_cli/main.py model=gpt-4o
   ```

   for full list of configs, see [config.py](src/llm_cli/config.py).

4. **Exit**:
   To exit the CLI, `Ctrl+C`.

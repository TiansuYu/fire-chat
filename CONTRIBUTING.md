# How to contribute to ChatGPT CLI

External contributes to this project are welcome! :heart: :heart:

## Philosophy

The philosophy behind this tool is to maintain simplicity while providing essential features for users who need to
interact with ChatGPT models from the command line efficiently. As explained in the README.md, we have undergone a
significant refactor to improve modularity and maintainability.

Our current approach emphasizes organizing code into logical directories, with each script ideally not exceeding 200-300
lines. This structure allows for better code organization, easier maintenance, and improved readability. Contributors
are encouraged to follow this modular approach when adding new features or making improvements.

We wanna to balance simplicity with functionality, ensuring that the tool remains user-friendly while accommodating the
growing feature set. When contributing, please consider how your changes fit into this modular structure and maintain
the tool's core philosophy of simplicity and efficiency.

## Development

Check out the repository:

`git clone https://github.com/TiansuYu/llm-cli`

Create an virtual environment and install all your dependencies:

`uv install`

After the changes are done don't forget to:

- update `README.md` if necessary
- update `pyproject.toml` with a new version number

- test if the installation as a package still works as expected using `uv install .` and running `llm-cli`

### Formatting

We use [pre-commit](https://pre-commit.com/) to ensure consistent code formatting and linting.

Please make sure to enable pre-commit hooks by:

```shell
uv run pre-commit install
```

To lint and format, run

```shell
uv run pre-commit run --all-files
```

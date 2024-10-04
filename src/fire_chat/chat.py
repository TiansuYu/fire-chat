import litellm
from pydantic import BaseModel, model_validator
from rich.markdown import Markdown

from fire_chat.config import Config
from fire_chat.tools.history import History
from fire_chat.message import Messages, Message

SYSTEM_PROMPT = (
    "Always use code blocks with the appropriate language tags. "
    "If asked for a table always format it using Markdown syntax."
)

SYSTEM_MESSAGE = Message(role="system", content=SYSTEM_PROMPT)


class LLMChat(BaseModel):
    config: Config
    messages: Messages = Messages()
    history: History | None = None
    system_message: Message = SYSTEM_MESSAGE

    @model_validator(mode="after")
    def load_history(self):
        """
        If no history is loaded or history has a different model, starts a new history session.
        Otherwise, load messages from history.
        """
        if self.history is None or self.history.model != self.config.model:
            # start a new history
            self.history = History(model=self.config.model)
        else:
            self.messages.extend(self.history.messages)

    def completion(self, message: Message | str = None, markdown: bool = True) -> Markdown | str:
        message = Message(role="user", content=message) if isinstance(message, str) else message
        self.messages.append(message)
        if "system" not in [message.role for message in self.messages]:
            self.messages.insert(0, self.system_message)

        response = litellm.completion(
            model=self.config.model,
            api_key=self.config.get_suitable_api_key(),
            temperature=self.config.temperature,
            messages=self.messages.model_dump(),  # noqa
            base_url=self.config.suitable_provider.proxy_url if self.config.suitable_provider.proxy_url else None,
        )

        # validate at least one choice exists
        if not response.choices:
            raise ValueError(f"Did not receive a valid choice from model '{self.config.model}'")

        # try update budget if budget is set
        if self.config.budget.is_on:
            self.config.budget.update_cost(response)
            self.config.budget.save()

        # parse and return response message, update existing messages
        resp_message = Message.model_validate(response.choices[0]["message"].model_dump())
        self.messages.append(resp_message)
        return Markdown(resp_message.content) if markdown else resp_message.content

    def save_history(self, path: str | None = None) -> None:
        if self.history is not None:
            self.history.messages.extend(self.messages)
            self.history.save(path)

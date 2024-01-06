from disnake import Option
from disnake.ext.cornsnake.types_ import SlashCommandCallbackType


class PendingSlashCommand:
    def __init__(self, callback: SlashCommandCallbackType) -> None:
        self.callback = callback
        self.options: list[Option] = []

    def add_option(self, option: Option) -> None:
        self.options.append(option)

class SlashCommand(PendingSlashCommand):
    def __init__(
        self,
        name: str,
        callback: SlashCommandCallbackType,
    ) -> None:
        super().__init__(callback)
        self.name = name

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from disnake import AppCmdInter, Option
    from .types_ import SlashCommandCallbackType


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

    @classmethod
    def from_pending(cls, name: str, pending: PendingSlashCommand) -> SlashCommand:
        command = cls(name, pending.callback)
        command.options = pending.options
        return command

    async def invoke(self, inter: AppCmdInter[Any]) -> None:
        self.callback(inter)

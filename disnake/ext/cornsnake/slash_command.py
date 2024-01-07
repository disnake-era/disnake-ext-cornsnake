# SPDX-License-Identifier: MIT

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from disnake import Option
    from disnake.ext.cornsnake.types_ import P, SlashCommandCallbackType
else:
    P = t.TypeVar("P")


class PendingSlashCommand(t.Generic[P]):
    def __init__(self, callback: SlashCommandCallbackType[P]) -> None:
        self.callback = callback
        self.options: list[Option] = []

    def add_option(self, option: Option) -> None:
        self.options.append(option)


class SlashCommand(PendingSlashCommand[P]):
    def __init__(
        self,
        name: str,
        callback: SlashCommandCallbackType[P],
    ) -> None:
        super().__init__(callback)
        self.name = name

    @classmethod
    def from_pending(cls, name: str, pending: PendingSlashCommand[P]) -> SlashCommand[P]:
        command = cls(name, pending.callback)
        command.options = pending.options
        return command

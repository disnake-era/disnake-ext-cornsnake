# SPDX-License-Identifier: MIT

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from disnake.app_commands import SlashCommand as DisnakeSlashCommand

if TYPE_CHECKING:
    from typing import Any

    from disnake import APISlashCommand, AppCmdInter, Option, Permissions
    from disnake.i18n import LocalizedRequired

    from .types_ import SlashCommandCallable


@dataclass
class PendingSlashCommand:
    cb: SlashCommandCallable
    options: list[Option]


class SlashCommand(DisnakeSlashCommand):
    def __init__(  # noqa: PLR0913
        self,
        name: LocalizedRequired,
        callback: SlashCommandCallable,
        /,
        description: LocalizedRequired,
        *,
        options: list[Option] | None = None,
        dm_permission: bool | None = None,
        default_member_permissions: Permissions | int | None = None,
        nsfw: bool | None = None,
        guild_ids: list[int] | None = None,
    ) -> None:
        super().__init__(name, description, options, dm_permission, default_member_permissions, nsfw)
        self.callback = callback
        self.guild_ids = guild_ids
        self._api: APISlashCommand | None = None

    async def invoke(self, inter: AppCmdInter[Any]) -> None:
        await self.callback(inter, **inter.options)

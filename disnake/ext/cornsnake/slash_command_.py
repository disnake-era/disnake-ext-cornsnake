# SPDX-License-Identifier: MIT

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic

from disnake import APISlashCommand
from disnake.app_commands import SlashCommand as DisnakeSlashCommand

if TYPE_CHECKING:
    from typing import Any

    from disnake import AppCmdInter, Option, Permissions
    from disnake.app_commands import APIApplicationCommand
    from disnake.i18n import LocalizedRequired

    from .types_ import CheckCallable, P, SlashCommandCallable


@dataclass
class PendingSlashCommand(Generic["P"]):
    cb: SlashCommandCallable
    checks: list[CheckCallable[P]]
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
    ) -> None:
        super().__init__(name, description, options, dm_permission, default_member_permissions, nsfw)
        self.callback = callback
        self._api: dict[int, APISlashCommand] = {}

    def upsert_api(self, api: APIApplicationCommand) -> None:
        if not isinstance(api, APISlashCommand):
            raise TypeError("Attempted to cache APIApplicationCommand that is not APISlashCommand. This is a bug.")

        self._api[api.guild_id or 0] = api

    @property
    def id(self) -> int | None:  # noqa: A003
        command = self._api.get(0)
        return command and command.id

    async def invoke(self, inter: AppCmdInter[Any]) -> None:
        await self.callback(inter, **inter.options)

class GuildSlashCommand(SlashCommand):
    def __init__(self, *args: Any, guild_ids: tuple[int], **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.guild_ids = guild_ids

    def get_id(self, guild_id: int) -> int | None:
        command = self._api.get(guild_id)
        return command and command.id

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, NewType

from asyncstdlib.builtins import all as async_all

from disnake.utils import maybe_coroutine

if TYPE_CHECKING:
    from typing import Any

    from disnake import AppCmdInter, Permissions
    from disnake.app_commands import APIApplicationCommand
    from disnake.i18n import LocalizedRequired

    from .types_ import AnyCheck, CommandCallable

@dataclass
class PendingCommand:
    callback: CommandCallable
    checks: list[AnyCheck]

class AppCommand:
    def __init__(
        self,
        name: LocalizedRequired,
        callback: CommandCallable,
        /,
        guild_ids: tuple[int] | None = None,
        *,
        dm_permission: bool = True,
        default_member_permissions: Permissions | None = None,
        nsfw: bool = False,
    ) -> None:
        self.name = name
        self.callback = callback
        self.checks: list[AnyCheck]
        self.dm_permission = dm_permission
        self.default_member_permissions = default_member_permissions
        self.nsfw = nsfw
        self.guild_ids = guild_ids
        self._api: dict[int, APIApplicationCommand]

    def upsert_api(self, api: APIApplicationCommand) -> None:
        self._api[api.guild_id or 0] = api

    def get_id(self, *, guild_id: int | None = None) -> int | None:
        if self.guild_ids and not guild_id:
            raise ValueError("This is a guild command, but `guild_id` was not passed.")

        command = self._api.get(guild_id or 0)
        return command and command.id

    async def invoke(self, inter: AppCmdInter[Any]) -> None:
        """Invoke the command."""
        if not await async_all(await maybe_coroutine(check, inter) for check in self.checks):
            return

        await self.callback(inter, **inter.options)

class SlashCommand(AppCommand):
    def __init__(
        self,
        name: LocalizedRequired,
        callback: CommandCallable,
        /,
        description: LocalizedRequired = "-",
        guild_ids: tuple[int] | None = None,
        *,
        dm_permission: bool = True,
        default_member_permissions: Permissions | None = None,
        nsfw: bool = False,
    ) -> None:
        super().__init__(
            name,
            callback,
            guild_ids,
            dm_permission=dm_permission,
            default_member_permissions=default_member_permissions,
            nsfw=nsfw,
        )
        self.description = description

UserCommand = NewType("UserCommand", AppCommand)
MessageCommand = NewType("MessageCommand", AppCommand)

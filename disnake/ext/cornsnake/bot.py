# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from disnake import Client

from .slash_command_ import GuildSlashCommand
from .utils import copy_sig

if TYPE_CHECKING:
    from typing import Any

    from typing_extensions import Self, TypeAlias, TypedDict

    from disnake import AppCmdInter

    from .slash_command_ import SlashCommand

    AnySlash: TypeAlias = "SlashCommand | GuildSlashCommand"

    class CommandDiff(TypedDict):
        to_upsert: list[AnySlash]
        to_delete: list[AnySlash]


async def command_diff(client: Client, local: list[AnySlash]) -> CommandDiff:
    diff: CommandDiff = { "to_upsert": [], "to_delete": [] }

    local_global_commands: set[SlashCommand] = set(filter(lambda cmd: not isinstance(cmd, GuildSlashCommand), local))  # type: ignore
    remote_global_command_names = tuple(cmd.name for cmd in await client.fetch_global_commands(with_localizations=False))

    # We assume all guilds the bot is in are cached already
    # guild_ids = tuple(guild.id for guild in client.guilds)

    for cmd in local_global_commands:
        if cmd.name not in remote_global_command_names:
            diff["to_delete"].append(cmd)

    for cmd

    return diff


class Bot(Client):
    @copy_sig(Client.__init__)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slash_commands: list[AnySlash] = []

    async def on_ready(self) -> None:
        await self.register_commands()

    async def on_application_command(self, inter: AppCmdInter[Self]) -> None:
        await self.process_commands(inter)

    async def register_commands(self) -> None:
        for slash in self.slash_commands:
            if isinstance(slash, GuildSlashCommand):
                apis = await asyncio.gather(*(self.create_guild_command(gid, slash) for gid in slash.guild_ids))
                for api in apis:
                    slash.upsert_api(api)
            else:
                await self.create_global_command(slash)

    async def process_commands(self, inter: AppCmdInter[Self]) -> None:
        for slash in self.slash_commands:
            if slash.name == inter.data.name:
                await slash.invoke(inter)

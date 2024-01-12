# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from disnake import Client

from .slash_command_ import GuildSlashCommand
from .utils import copy_sig

if TYPE_CHECKING:
    from typing import Any

    from typing_extensions import Self

    from disnake import AppCmdInter

    from .types_ import AnySlash


class Bot(Client):
    @copy_sig(Client.__init__)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slash_commands: list[AnySlash] = []

    def add_slash_command(self, command: AnySlash) -> None:
        self.slash_commands.append(command)

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
                if isinstance(slash, GuildSlashCommand) and not inter.guild_id in slash.guild_ids:
                    continue

                await slash.invoke(inter)

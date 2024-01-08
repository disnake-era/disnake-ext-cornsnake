# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from disnake import Client

from .utils import copy_sig

if TYPE_CHECKING:
    from typing import Any

    from typing_extensions import Self

    from disnake import AppCmdInter

    from .slash_command_ import SlashCommand


class Bot(Client):
    @copy_sig(Client.__init__)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slash_commands: list[SlashCommand] = []


    async def on_ready(self) -> None:
        await self.register_commands()


    async def on_application_command(self, inter: AppCmdInter[Self]) -> None:
        await self.process_commands(inter)


    async def register_commands(self) -> None:
        for slash in self.slash_commands:
            if slash.guild_ids:
                await asyncio.gather(self.create_guild_command(gid, slash) for gid in slash.guild_ids)
            else:
                await self.create_global_command(slash)


    async def process_commands(self, inter: AppCmdInter[Self]) -> None:
        for slash in self.slash_commands:
            if slash.name == inter.data.name:
                await slash.invoke(inter)

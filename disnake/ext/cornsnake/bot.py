# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from disnake import Client, Event

from .errors import CheckError
from .slash_command_ import GuildSlashCommand
from .utils import copy_sig

if TYPE_CHECKING:
    from typing import Any

    from typing_extensions import Self

    from disnake import AppCmdInter

    from .types_ import AnySlashCmd, AnyUserCmd, AnyMessageCmd


class Bot(Client):
    """A client subclass that provides methods for command registration and processing.

    Attributes
    ----------
    slash_commands: :class:`list`[:class:`SlashCommand` | :class:`GuildSlashCommand`]
        List of attached slash commands.

    user_commands: :class:`list`[:class:`UserCommand` | :class:`GuildUserCommand`]
        List of attached user commands.

    message_commands: :class:`list`[:class:`MessageCommand` | :class:`GuildMessageCommand`]
        List of attached message commands.
    """

    @copy_sig(Client.__init__)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slash_commands: list[AnySlashCmd] = []
        self.user_commands: list[AnyUserCmd] = []
        self.message_commands: list[AnyMessageCmd] = []

    async def register_commands(self) -> None:
        """Register all attached commands."""
        for slash in self.slash_commands:
            if isinstance(slash, GuildSlashCommand):
                apis = await asyncio.gather(*(self.create_guild_command(gid, slash) for gid in slash.guild_ids))
                for api in apis:
                    slash.upsert_api(api)
            else:
                await self.create_global_command(slash)

    async def process_command(self, inter: AppCmdInter[Self]) -> None:
        """Map interaction to local command and invoke it."""
        for slash in self.slash_commands:
            if slash.name == inter.data.name:
                if isinstance(slash, GuildSlashCommand) and inter.guild_id not in slash.guild_ids:
                    continue

                try:
                    await slash.invoke(inter)
                except CheckError as e:
                    self.dispatch("check_error", e)

class ManagedBot(Bot):
    """A :class:`Bot` subclass with automatic command registration and processing.
    
    Registration and processing happen on :attr:`Event.ready` and
    :attr:`Event.application_command` resprectively.
    """

    @copy_sig(Bot.__init__)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.add_listener(self.register_commands, Event.ready)
        self.add_listener(self.process_command, Event.application_command)

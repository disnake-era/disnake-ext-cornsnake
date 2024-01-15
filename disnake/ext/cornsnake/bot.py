# SPDX-License-Identifier: MIT

from __future__ import annotations
import asyncio

from itertools import chain
from typing import TYPE_CHECKING, cast

from disnake import Client, Event

from .app_commands import MessageCommand, SlashCommand, UserCommand, AppCommand
from .errors import CheckError
from .utils import copy_sig

if TYPE_CHECKING:
    from typing import Any

    from typing_extensions import Self

    from disnake import AppCmdInter


class Bot(Client):
    """A client subclass that provides methods for command registration and processing.

    Attributes
    ----------
    slash_commands: :class:`list`[:class:`SlashCommand`]
        List of attached slash commands.

    user_commands: :class:`list`[:class:`UserCommand`]
        List of attached user commands.

    message_commands: :class:`list`[:class:`MessageCommand`]
        List of attached message commands.
    """

    @copy_sig(Client.__init__)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slash_commands: list[SlashCommand] = []
        self.user_commands: list[UserCommand] = []
        self.message_commands: list[MessageCommand] = []

    @property
    def app_commands(self) -> chain[AppCommand]:
        return chain(cast("tuple[AppCommand, ...]", (self.slash_commands, self.user_commands, self.message_commands)))

    async def register_commands(self) -> None:
        """Register all attached commands."""
        for command in self.app_commands:
            if command.guild_ids:
                apis = await asyncio.gather(*(self.create_guild_command(guild_id, command.to_payload()) for guild_id in command.guild_ids))

    async def process_command(self, inter: AppCmdInter[Self]) -> None:
        """Map interaction to local command and invoke it."""
        for slash in self.slash_commands:
            if slash.name == inter.data.name:
                if slash.guild_ids and inter.guild_id not in slash.guild_ids:
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

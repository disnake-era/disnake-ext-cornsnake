# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from typing import Any, Callable

    from typing_extensions import TypeAlias

    from disnake import AppCmdInter

    from .bot import Bot
    from .slash_command_ import GuildSlashCommand, SlashCommand, UserCommand, GuildUserCommand, MessageCommand, GuildMessageCommand

    AnySlashCmd: TypeAlias = "SlashCommand | GuildSlashCommand"
    AnyUserCmd: TypeAlias = "UserCommand | GuildUserCommand"
    AnyUserCmd: TypeAlias = "MessageCommand | GuildMessageCommand"

    CornInter = AppCmdInter[Bot]
    LambdaCheck = Callable[[CornInter], bool]
    CheckCallable = Callable[[CornInter], Awaitable[bool]]
    SlashCommandCallable: TypeAlias = Callable[..., Awaitable[Any]]

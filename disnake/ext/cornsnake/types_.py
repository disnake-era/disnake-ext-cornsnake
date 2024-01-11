# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from typing import Any, Callable

    from typing_extensions import TypeAlias

    from .slash_command_ import GuildSlashCommand, SlashCommand

    AnySlash: TypeAlias = "SlashCommand | GuildSlashCommand"
    SlashCommandCallable = Callable[..., Awaitable[Any]]

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Awaitable, Callable

    from .decorators import PendingSlashCommand

    SlashCommandCallbackType = Callable[..., Awaitable[Any]]
    PendingCallback = PendingSlashCommand | SlashCommandCallbackType

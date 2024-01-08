# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from typing import Any, Callable

    SlashCommandCallable = Callable[..., Awaitable[Any]]

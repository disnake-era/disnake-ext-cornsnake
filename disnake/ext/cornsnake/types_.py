# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from typing import Any, Callable

    from typing_extensions import TypeAlias

    from disnake import AppCmdInter

    from .bot import Bot

    AnyCheck: TypeAlias = "LambdaCheck | AsyncCheck"

    CornInter = AppCmdInter[Bot]
    LambdaCheck = Callable[[CornInter], bool]
    AsyncCheck = Callable[[CornInter], Awaitable[bool]]
    CommandCallable: TypeAlias = Callable[..., Awaitable[Any]]

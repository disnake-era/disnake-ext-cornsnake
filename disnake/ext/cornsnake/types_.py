# SPDX-License-Identifier: MIT

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from typing_extensions import Concatenate, ParamSpec

    from disnake import AppCmdInter

    from .decorators import PendingSlashCommand

    P = ParamSpec("P", default=[AppCmdInter])

    SlashCommandCallbackType = t.Callable[Concatenate[P], t.Awaitable[t.Any]]
    PendingCallback = PendingSlashCommand[P] | SlashCommandCallbackType[P]

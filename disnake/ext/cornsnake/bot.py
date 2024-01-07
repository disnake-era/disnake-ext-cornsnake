# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import Client

from .utils import copy_sig

if TYPE_CHECKING:
    from typing import Any

    from disnake.ext.cornsnake.slash_command import SlashCommand


class Bot(Client):
    @copy_sig(Client.__init__)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.slash_commands: list[SlashCommand] = []

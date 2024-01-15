from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

from disnake.app_commands import ApplicationCommand

if TYPE_CHECKING:
    from .types_ import CheckCallable, LambdaCheck, SlashCommandCallable

@dataclass
class PendingAppCommand:
    cb: SlashCommandCallable
    checks: list[CheckCallable | LambdaCheck]


class AppCommand(ApplicationCommand):
    pass

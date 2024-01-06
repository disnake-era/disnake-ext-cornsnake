from __future__ import annotations
from typing import Callable

from .slash_command import PendingSlashCommand, SlashCommand
from .types_ import SlashCommandCallbackType

def slash_command(name: str | None = None) -> Callable[[PendingSlashCommand | SlashCommandCallbackType]]:
    def decorator(pending: PendingSlashCommand | SlashCommandCallbackType) -> 

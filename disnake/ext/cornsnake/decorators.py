# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import Option, OptionType

from .slash_command import PendingSlashCommand, SlashCommand

if TYPE_CHECKING:
    from typing import Callable

    from .types_ import P, PendingCallback


def slash_command(name: str | None = None) -> Callable[[PendingCallback[P]], SlashCommand[P]]:
    def decorator(pending: PendingCallback[P]) -> SlashCommand[P]:
        name_ = name or pending.__name__
        return (
            SlashCommand(name_, pending)
            if callable(pending)
            else SlashCommand.from_pending(name_, pending)
        )

    return decorator


def with_option(
    name: str,
    type_: OptionType,
    /,
    description: str | None = None,
    *,
    required: bool = False,
) -> Callable[[PendingCallback[P]], PendingSlashCommand[P]]:
    def decorator(pending: PendingCallback[P]) -> PendingSlashCommand[P]:
        command = PendingSlashCommand(pending) if callable(pending) else pending
        command.add_option(
            Option(name=name, type=type_, description=description, required=required)
        )
        return command

    return decorator

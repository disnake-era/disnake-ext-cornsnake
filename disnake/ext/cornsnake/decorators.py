# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

from disnake import Option, OptionType

from .slash_command_ import PendingSlashCommand, SlashCommand

if TYPE_CHECKING:
    from typing import Any, Callable

    from .types_ import SlashCommandCallable


def slash_command(name: str, **kwargs: Any) -> Callable[[SlashCommandCallable | PendingSlashCommand], SlashCommand]:
    def decorator(cb: SlashCommandCallable | PendingSlashCommand) -> SlashCommand:
        if callable(cb):
            slash = SlashCommand(name, cb, **kwargs)
        else:
            slash = SlashCommand(name, cb.cb, **kwargs)
            slash.options = cb.options

        return slash

    return decorator


def with_option(
    name: str,
    type_: OptionType,
    /,
    description: str | None = None,
    *,
    required: bool = False,
) -> Callable[[SlashCommandCallable | PendingSlashCommand], PendingSlashCommand]:
    def decorator(cb: SlashCommandCallable | PendingSlashCommand) -> PendingSlashCommand:
        option = Option(name, description, type_, required)

        if callable(cb):
            cb = PendingSlashCommand(cb, [option])
        else:
            cb.options.append(option)

        return cb

    return decorator

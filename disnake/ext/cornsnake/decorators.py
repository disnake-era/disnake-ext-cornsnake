# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, overload

from disnake import Option, OptionType

from .slash_command_ import GuildSlashCommand, PendingSlashCommand, SlashCommand

if TYPE_CHECKING:
    from typing import Any, Callable

    from disnake import Permissions
    from disnake.i18n import LocalizedRequired

    from .types_ import SlashCommandCallable

# NOTE: order matters! apparently..
@overload
def slash_command(
    name: LocalizedRequired,
    /,
    description: LocalizedRequired,
    *,
    options: list[Option] | None = None,
    dm_permission: bool | None = None,
    default_member_permissions: Permissions | int | None = None,
    nsfw: bool | None = None,
    guild_ids: None = ...,
) -> Callable[[SlashCommandCallable | PendingSlashCommand], SlashCommand]: ...

@overload
def slash_command(
    name: LocalizedRequired,
    /,
    description: LocalizedRequired,
    *,
    options: list[Option] | None = None,
    dm_permission: bool | None = None,
    default_member_permissions: Permissions | int | None = None,
    nsfw: bool | None = None,
    guild_ids: tuple[int] = ...,
) -> Callable[[SlashCommandCallable | PendingSlashCommand], GuildSlashCommand]: ...

def slash_command(name: LocalizedRequired, /, *args: Any, **kwargs: Any) -> Callable[[SlashCommandCallable | PendingSlashCommand], SlashCommand | GuildSlashCommand]:
    def decorator(cb: SlashCommandCallable | PendingSlashCommand) -> SlashCommand:
        per_guild = "guild_ids" in kwargs and kwargs.get("guild_ids") is not None
        class_ = GuildSlashCommand if per_guild else SlashCommand

        if callable(cb):
            slash = class_(name, cb, *args, **kwargs)
        else:
            slash = class_(name, cb.cb, *args, **kwargs)
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

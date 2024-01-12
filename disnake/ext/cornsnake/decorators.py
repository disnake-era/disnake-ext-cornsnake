# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, overload

from disnake import Option, OptionType

from .slash_command_ import GuildSlashCommand, PendingSlashCommand, SlashCommand

if TYPE_CHECKING:
    from typing import Any, Callable

    from disnake import Permissions
    from disnake.i18n import LocalizedRequired

    from .types_ import CheckCallable, P, SlashCommandCallable

# NOTE: overload order matters! apparently..
# NOTE: [P]s not specified here as @slash_command is the command finalization step
# and after it no options or checks can be added (and therefore checked).
@overload
def slash_command(
    name: LocalizedRequired,
    /,
    description: LocalizedRequired,
    *,
    dm_permission: bool = False,
    default_member_permissions: Permissions | None = None,
    nsfw: bool | None = None,
    guild_ids: None = ...,
) -> Callable[[SlashCommandCallable | PendingSlashCommand], SlashCommand]: ...

@overload
def slash_command(
    name: LocalizedRequired,
    /,
    description: LocalizedRequired = "-",
    *,
    dm_permission: bool = False,
    default_member_permissions: Permissions | None = None,
    nsfw: bool | None = None,
    guild_ids: list[int] = ...,
) -> Callable[[SlashCommandCallable | PendingSlashCommand], GuildSlashCommand]: ...

def slash_command(name: LocalizedRequired, /, *args: Any, **kwargs: Any) -> Callable[[SlashCommandCallable | PendingSlashCommand], SlashCommand | GuildSlashCommand]:
    """Finalize all pending options and checks (if any) into a slash command.

    Collects all pending slash command options and checks into a :class:`SlashCommand`
    that can afterwards be added to a :class:`Bot` or invoked manually.

    Parameters
    ----------
    name: :class:`str` | :class:`disnake.Localized`
        Command's name.
    description: :class:`str` | :class:`disnake.Localized`
        Command's description. Cannot be "truly" absent due to Discord limitations
        and therefore defaults to "-".
    dm_permission: :class:`bool`
        Whether this command can be used in DMs. Defaults to ``True``.
    default_member_permissions: :class:`Permissions` | :class:`None`
        
    """
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
) -> Callable[[SlashCommandCallable[P] | PendingSlashCommand[P]], PendingSlashCommand[P]]:
    """Add an option to the slash conmand.

    Each command option must have a corresponding same-named parameter
    in slash command's callback that can be passed by keyword.

    Parameters
    ----------
    name: :class:`str`
        Option's name.
    type_: :class:`OptionType`
        Option's type.
    description: :class:`str` | :class:`None`
        Option's description.
    required: :class:`bool`
        Whether the option is required. If the option is not required,
        the corresponding slash command's parameter must have a default
        specified. Defaults to ``False``.
    """
    def decorator(cb: SlashCommandCallable[P] | PendingSlashCommand[P]) -> PendingSlashCommand:
        option = Option(name, description, type_, required)
    
        if callable(cb):
            cb = PendingSlashCommand(cb, [], [option])
        else:
            cb.options.append(option)

        return cb
    return decorator


def with_check(
    check: CheckCallable[P]
) -> Callable[[SlashCommandCallable[P] | PendingSlashCommand[P]], PendingSlashCommand[P]]:
    """Add a pre-run check to slash command.

    Commands checks are run from top to bottom in the same order
    as they were specified on this specific command. Slash
    command's callback is only executed if all checks pass.

    Parameters
    ----------
    check: (**P) -> bool
        The check. Check's signature must be compatible with
        the signature of slash command's callback.

    Returns
    -------
    :class:`PendingSlashCommand`
        The updated slash command factory.
    """
    def decorator(cb: SlashCommandCallable[P] | PendingSlashCommand[P]) -> PendingSlashCommand[P]:
        if callable(cb):
            cb = PendingSlashCommand(cb, [check], [])
        else:
            cb.checks.append(check)

        return cb
    return decorator

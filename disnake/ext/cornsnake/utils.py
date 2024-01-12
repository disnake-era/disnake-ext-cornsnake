# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, TypeVar, cast

from asyncstdlib.itertools import chain

from .slash_command_ import GuildSlashCommand

T = TypeVar("T")

if TYPE_CHECKING:
    from typing import Any

    from typing_extensions import ParamSpec, TypeAlias, TypedDict

    from disnake import Client
    from disnake.app_commands import APISlashCommand

    from .types_ import AnySlash

    P = ParamSpec("P")

    # list of (command_name, guild_id if command is GuildCommand else None)
    CommandOperational: TypeAlias = "list[tuple[str, int | None]]"

    class CommandDiff(TypedDict):
        to_upsert: CommandOperational
        to_delete: CommandOperational


def copy_sig(_: Callable[P, Any]) -> Callable[[Callable[..., T]], Callable[P, T]]:
    def inner(func: Callable[..., T]) -> Callable[P, T]:
        return cast("Callable[P, T]", func)
    return inner


async def fetch_guild_commands(client: Client) -> chain[APISlashCommand]:
    # Assume that all guilds the bot is in are cached; not sure how much of an issue this is
    guild_ids = (guild.id for guild in client.guilds)
    commands = (await client.fetch_guild_commands(gid) for gid in guild_ids)
    return cast("chain[APISlashCommand]", chain.from_iterable(commands))


def is_remote_command_outdated(remote: APISlashCommand, local: AnySlash) -> bool:
    return any((
        remote.default_member_permissions != local.default_member_permissions,
        remote.description_localizations != local.description_localizations,
        remote.description != local.description,
        remote.dm_permission != local.dm_permission,
        remote.name != local.name,
        remote.name_localizations != local.name_localizations,
        remote.nsfw != local.nsfw,
        remote.options != local.options,
    ))


async def commands_diff(client: Client, local: list[AnySlash]) -> CommandDiff:
    diff: CommandDiff = {"to_upsert": [], "to_delete": []}

    local_global_commands = {cmd.name: cmd for cmd in local if not isinstance(cmd, GuildSlashCommand)}
    local_guild_commands = {cmd.name: cmd for cmd in local if isinstance(cmd, GuildSlashCommand)}

    remote_global_commands = cast("list[APISlashCommand]", await client.fetch_global_commands(with_localizations=False))
    remote_guild_commands = await fetch_guild_commands(client)

    # For every remote global command
    for remote_global_command in remote_global_commands:
        # Try to find a matching local global command
        local_global_command = local_global_commands.get(remote_global_command.name)

        # If it's not defined locally anymore, mark it for deletion
        if not local_global_command:
            diff["to_delete"].append((remote_global_command.name, None))
            continue

        # If the remote version is different from the local one, mark it for update
        if is_remote_command_outdated(remote_global_command, local_global_command):
            diff["to_upsert"].append((remote_global_command.name, None))
            continue

    # For every remote guild command
    async for remote_guild_command in remote_guild_commands:
        # Try to find a matching local guild command
        local_guild_command = local_guild_commands.get(remote_guild_command.name)

        # If it's not defined locally anymore, mark it for deletion
        if not local_guild_command:
            diff["to_delete"].append((remote_guild_command.name, remote_guild_command.guild_id))
            continue

        # If it's still defined locally, but for a different guild, mark it for deletion as well
        if remote_guild_command.guild_id not in local_guild_command.guild_ids:
            diff["to_delete"].append((remote_guild_command.name, remote_guild_command.guild_id))
            continue

        # If the remote version is different from the local one, mark it for update
        if is_remote_command_outdated(remote_guild_command, local_guild_command):
            diff["to_upsert"].append((remote_guild_command.name, None))
            continue

    return diff

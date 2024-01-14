# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
import os

from disnake import AppCmdInter, OptionType
from disnake.ext import cornsnake


async def isnt_owner(inter: AppCmdInter[cornsnake.Bot]) -> bool:
    return bool(inter.guild and inter.guild.owner_id != inter.author.id)

@cornsnake.slash_command("idk", "-")
@cornsnake.with_option("boolean", OptionType.boolean, "just enter it")
@cornsnake.with_check(isnt_owner)
async def idkcmd(inter: AppCmdInter[cornsnake.Bot], *, boolean: bool = False) -> None:
    await inter.response.send_message(f"Hi from cornsnake! boolean is {boolean}")

async def main() -> None:
    bot = cornsnake.Bot()

    bot.slash_commands.append(idkcmd)

    await bot.start(os.environ["BOT_TOKEN"])


asyncio.run(main())

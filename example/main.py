# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
import os

from disnake import AppCmdInter, OptionType
from disnake.ext import cornsnake


async def main() -> None:
    bot = cornsnake.Bot()

    @cornsnake.slash_command("idk")
    @cornsnake.with_option("boolean", OptionType.boolean, "just enter it")
    async def idkcmd(inter: AppCmdInter[cornsnake.Bot], *, boolean: bool = False) -> None:
        await inter.response.send_message(f"Hi from cornsnake! boolean is {boolean}")

    bot.slash_commands.append(idkcmd)

    await bot.start(os.environ["BOT_TOKEN"])


asyncio.run(main())

# SPDX-License-Identifier: MIT

import asyncio

from disnake.ext import cornsnake


async def main() -> None:
    bot = cornsnake.Bot()

    await bot.start("TOKEN")


asyncio.run(main())

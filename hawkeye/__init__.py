from .hawkeye import Hawkeye

async def setup(bot): # async
  await bot.add_cog(Hawkeye(bot)) # await
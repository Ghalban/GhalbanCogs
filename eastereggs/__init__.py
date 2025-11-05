from .eastereggs import EasterEggs

async def setup(bot): # async
  await bot.add_cog(EasterEggs(bot)) # await
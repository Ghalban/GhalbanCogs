from .animod import AniMod

async def setup(bot): # async
  await bot.add_cog(AniMod(bot)) # await
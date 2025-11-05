from .instareelfixer import InstaReelFixer

async def setup(bot):
  await bot.add_cog(InstaReelFixer(bot))
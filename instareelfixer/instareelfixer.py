from redbot.core import commands
import discord
import re

class InstaReelFixer(commands.Cog):
    """Fixes Instagram Reels links for better Discord embeds. Skips DMs and already-fixed links."""

    def __init__(self, bot):
        self.bot = bot
        # Skip ddinstagram links using negative lookahead
        self.pattern = re.compile(r'https?://(?!dd)(?:www\.)?instagram\.com/reel/[\w\-]+(?:[/?][^\s>]*)?')

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bots and DMs
        if message.author.bot or message.guild is None:
            return

        links = self.pattern.findall(message.content)
        if not links:
            return

        try:
            await message.delete()
        except discord.Forbidden:
            return  # Bot can’t delete message

        fixed_text = self.pattern.sub(
            lambda m: m.group(0).replace("instagram.com", "ddinstagram.com"), message.content
        )

        response = f"📸 {message.author.mention} said:\n{fixed_text}\n-# :bulb: **Tip:** type `dd` before `instagram` in reel links to avoid embed fails."
        await message.channel.send(response)

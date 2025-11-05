from redbot.core import commands
import discord
import time
import random
import re

class EasterEggs(commands.Cog):
    """Responds to inside jokes with custom replies. Guild-restricted, cooldown-enabled, and chaos-infused."""

    def __init__(self, bot):
        self.bot = bot
        # You can assign either a single string or a list of options for each trigger
        self.responses = {
            "snack": ["NO. Do NOT eat that!", "I'd eat it.", "Looks delicious.", "Yum!"],
            "water": ["Take a sip of water NOW!", "I'm so thirsty.", "Gotta stay hydrated!"],
            "food": ["I'm so hungry.", "Can I have some?", "Gimme some of that." ],
            "hawkboy": ["You called?", "I'm watching you.", "Love ya.", "uwu", "owo"],
            "gryphon": ["You called?", "Gryphon is me.", "You called?", "I'm part barbary falcon and part african wolf."],
            "good morning": ["Good morning!", "Top of the morning to you laddies!"],
            "good night": ["Justice never sleeps.", "nini uwu"],
            "keven": ["https://cdn.discordapp.com/attachments/487841462478831628/752342860191498260/Screen_Shot_2020-09-06_at_9.40.09_PM.png?ex=68560de3&is=6854bc63&hm=4997ffc6d0121d6dcef04a87c416cbb9804d7db7d61ac4911e73f1cd0d3cbaab&"]
        }
        self.cooldowns = {}  # {channel_id: timestamp}
        self.cooldown_duration = 30  # seconds
        self.allowed_guild_id = 487841462478831626  # Only works in A&I

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        if message.guild.id != self.allowed_guild_id:
            return

        now = time.time()
        self.cooldowns = {
            k: v for k, v in self.cooldowns.items() if now - v < self.cooldown_duration
        }

        if self.cooldowns.get(message.channel.id):
            return

        content = message.content
        for trigger, replies in self.responses.items():
            # Use regex to detect trigger words as whole phrases, ignoring punctuation
            pattern = r'\b' + re.escape(trigger) + r'\b'
            if re.search(pattern, content, re.IGNORECASE):
                if random.random() < 0.6:  # Chaos coinflip (60% chance to respond)
                    return
                self.cooldowns[message.channel.id] = now
                if isinstance(replies, list):
                    await message.channel.send(random.choice(replies))
                else:
                    await message.channel.send(replies)
                break
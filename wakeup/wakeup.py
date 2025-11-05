from redbot.core import commands
import discord
import asyncio
import time
import random
import logging
from typing import Optional

log = logging.getLogger(__name__)


class WakeUp(commands.Cog):
    """WakeUp cog — watches a configured channel and posts a random 'wake up' message after 6 hours of silence.

    Configure by editing attributes in __init__ or add commands later to manage them at runtime:
    - general_channel_id: int or None (channel to monitor)
    - allowed_guild_id: int or None (restrict to a single guild)
    - idle_responses: list[str] (messages to choose from)
    - idle_threshold_seconds: int (seconds of silence before sending; default 6 hours)
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # general channel to monitor for activity
        self.general_channel_id: Optional[int] = 487841462478831628
        self.allowed_guild_id: Optional[int] = 487841462478831626

        # Messages to pick from when posting to wake the channel
        self.idle_responses = [
            "**Tip:** You can share interesting articles or resources in <#487848221608116224> to help others learn and make! You can also start or add to [resource threads](https://support.discord.com/hc/en-us/articles/4403205878423-Threads-FAQ) to keep things organized. For example, check out https://ptb.discord.com/channels/487841462478831626/1364249024990810194",
            ":cricket:",
            "Is anyone there?",
            "Anyone still awake?",
            "It's been quiet here...",
            ":cricket: :cricket:",
            "**Tip:** You can invite others to chat in the <#704867340818448585> channel whenever you'd like!",
            "Is anyone out there?",
            "What have you been working on lately?",
            "Any cool ideas brewing?",
            "Any fun projects going on?",
            "What are you up to?",
            "Hey guys! How's it going?",
            "**Tip:** Found a great book? Tell us about it in <#613555438902050859>!",
            "<:z_1_pain_and_sorrow:699749910513320058>",
            "**Tip:** You can request a <#1021258823526256681> to help refine your work! Be specific about what kind of feedback you're looking for in the post topic and tags for the best experience. You can also link the thread along with your WIP in <#766149982092132352> to make it easier for others to find and contribute!",
            "Did you hear the news?",
            "Who's still awake?",
            "Guys???",
            "**Tip:** Stuck on what to draw? Head to <#646357371387641857> and use the `/artprompt` command to get a random prompt to spark your creativity!",
            "Hello???",
            "**Tip:**  You can post art updates, even small ones, in <#766149982092132352> to share your progress with others!",
            "It's awfully quiet...",
            "<:z_cringe:599047914261839892>",
            ":cricket: :cricket: :cricket:",
            "Wake up!!!!!",
            "Is someone there?",
            "**Tip:** If a message gets enough reactions of :star:, :heart:, or <:z_joy:746894566308970578> it will be featured in <#799882888311996416>!",
            "**Tip:** You can ask pertinent questions in <#1020745682463768807> to get help and advice from the community! Be sure to check out the [pinned message](https://ptb.discord.com/channels/487841462478831626/1020803043652030588) and existing threads for answers too.",
            "Just checking in... still quiet",
            "<:z_1_pain:682823256646221837>",
            "**Tip:** Try typing something!",
            "Hey. How's your day been so far?",
            ":cricket: :cricket: :cricket: :cricket:",
            "What's one small win you had today?",
            "Big or small, art or not, what are you working on today?",
            "<:y_Kermit_tired:854762076601057360>",
            "**Tip:** Found something that inspired you? Tell us about it in <#555936817652695040> so others can check it out too!",
        ]

        # Idle threshold in seconds (6 hours)
        self.idle_threshold_seconds = 6 * 3600

        # Tracks last seen non-bot activity timestamp (epoch seconds) for the monitored channel
        self.last_activity: Optional[float] = None

        # Flag to record that the cog has sent a wakeup message and is waiting for human activity
        self._wakeup_sent: bool = False

        # Background task handle
        self._task: Optional[asyncio.Task] = self.bot.loop.create_task(
            self._idle_announce_loop())

    def cog_unload(self):
        # Cancel the background task when the cog is unloaded
        try:
            if self._task and not self._task.done():
                self._task.cancel()
        except Exception:
            pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore DMs and bot messages
        if message.author.bot or message.guild is None:
            return

        # If configured, only watch a specific guild
        if self.allowed_guild_id and message.guild.id != self.allowed_guild_id:
            return

        # If monitoring a specific channel, update last_activity only when messages appear there
        if self.general_channel_id and message.channel.id == self.general_channel_id:
            # Human posted: update last_activity and clear wakeup flag so future idle periods can trigger again
            self.last_activity = time.time()
            self._wakeup_sent = False

    async def _initialize_last_activity(self, channel: discord.abc.Messageable):
        """Set last_activity from recent non-bot messages in the channel; fallback to now."""
        try:
            # Use TextChannel.history for TextChannel / Thread.history for threads; Messageable supports history
            async for msg in channel.history(limit=50):
                if not msg.author.bot:
                    self.last_activity = msg.created_at.timestamp()
                    return
        except Exception as e:
            log.debug(
                "WakeUp: unable to read channel history for initialization: %s", e)
        # fallback to now so we don't immediately post on startup if channel is unusable
        self.last_activity = time.time()

    async def _idle_announce_loop(self):
        """Background loop: send a random message to the monitored channel after idle_threshold_seconds of silence."""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                if not self.general_channel_id:
                    # Disabled; sleep and re-check periodically
                    await asyncio.sleep(600)
                    continue

                # Try to get the channel (cached first)
                channel = self.bot.get_channel(self.general_channel_id)
                if channel is None:
                    # Fetch from API if not cached
                    try:
                        channel = await self.bot.fetch_channel(self.general_channel_id)
                    except Exception as e:
                        log.warning(
                            "WakeUp: failed to fetch channel %s: %s", self.general_channel_id, e)
                        await asyncio.sleep(600)
                        continue

                # Ensure the channel supports history/send
                if not hasattr(channel, "history") or not hasattr(channel, "send"):
                    log.warning(
                        "WakeUp: configured channel %s is not a messageable channel", self.general_channel_id)
                    await asyncio.sleep(600)
                    continue

                # Initialize last_activity if needed
                if self.last_activity is None:
                    await self._initialize_last_activity(channel)

                now = time.time()
                idle_for = now - (self.last_activity or now)

                # If we've already sent a wakeup and no human has replied yet, do not send again
                if self._wakeup_sent:
                    # Sleep until something changes (either a human message will reset the flag via on_message,
                    # or we will periodically re-check). Sleeping a bit avoids tight-loop.
                    await asyncio.sleep(600)
                    continue

                if idle_for >= self.idle_threshold_seconds:
                    if not self.idle_responses:
                        log.debug(
                            "WakeUp enabled but idle_responses is empty.")
                    else:
                        message = random.choice(self.idle_responses)
                        try:
                            await channel.send(message)
                            log.info("WakeUp: sent idle message to channel %s after %.0f seconds of silence", getattr(
                                channel, "id", "unknown"), idle_for)
                            # Do NOT update self.last_activity here — we must not count our own message as human activity.
                            # Instead, set the wakeup flag so we don't spam messages repeatedly.
                            self._wakeup_sent = True
                        except discord.Forbidden:
                            log.warning("WakeUp: missing permission to send messages in channel %s", getattr(
                                channel, "id", "unknown"))
                        except Exception as e:
                            log.exception(
                                "WakeUp: failed to send message: %s", e)
                    # After sending, sleep a while to avoid spamming if sending repeatedly fails or no activity resumes
                    await asyncio.sleep(600)
                else:
                    # Sleep until the threshold would be reached, but wake periodically to pick up activity updates
                    remaining = self.idle_threshold_seconds - idle_for
                    await asyncio.sleep(min(300, remaining))
            except asyncio.CancelledError:
                break
            except Exception as e:
                log.exception(
                    "WakeUp: unexpected exception in idle loop: %s", e)
                await asyncio.sleep(300)

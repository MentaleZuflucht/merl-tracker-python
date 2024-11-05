from discord.ext import commands
import logging
import discord
import time


class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_logger = logging.getLogger('bot.events')
        self.message_timestamp = None

    @commands.Cog.listener()
    async def on_ready(self):
        """Logs bot readiness and initiates archiving if enabled."""
        self.bot_logger.info(f'Logged in as {self.bot.user}')
        self.bot_logger.info('Bot ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        """Records the timestamp when a message is sent."""
        if message.author == self.bot.user:
            return
        self.message_timestamp = time.time()
        self.bot_logger.info(f'Message received from {message.author} at {self.message_timestamp}')

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        """Sends a message if a specific user comes online within a specified time after a message is sent."""
        user_id = self.bot.config.user_id
        countdown = self.bot.config.countdown

        if after.id == user_id and before.status != discord.Status.online and after.status == discord.Status.online:
            if self.message_timestamp:
                time_taken = time.time() - self.message_timestamp
                if time_taken <= countdown:
                    self.bot_logger.info(f'User {after.name} came online within {time_taken:.2f} seconds')
                    channel = self.bot.get_channel(self.bot.config.channel_id)
                    if channel:
                        await channel.send(f'{after.name} came online {time_taken:.2f} seconds after the message')
                else:
                    self.bot_logger.info(f'User {after.name} came online after {time_taken:.2f} seconds')
                self.message_timestamp = None


def setup(bot):
    bot.add_cog(BotEvents(bot))

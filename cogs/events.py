from discord.ext import commands
import logging
import discord
import time


class BotEvents(commands.Cog):
    def __init__(self, bot):
        """
        Initialize the BotEvents cog.

        Args:
            bot: The Discord bot instance.
        """
        self.bot = bot
        self.bot_logger = logging.getLogger('bot.events')
        self.message_timestamp = None
        self.last_channel_id = None
        self.user_was_online = False

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Handle the bot's ready event.

        Logs when the bot has successfully logged in and is ready to receive events.
        """
        self.bot_logger.info(f'Logged in as {self.bot.user}')
        self.bot_logger.info('Bot ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Handle incoming messages.

        Records the timestamp and channel ID when a message is sent, excluding messages
        from the bot itself.

        Args:
            message (discord.Message): The message object containing information about
                the received message.
        """
        if message.author == self.bot.user:
            return

        # Check if the target user is already online when message is received
        target_user = message.guild.get_member(self.bot.config.user_id)
        if target_user and target_user.status == discord.Status.online:
            self.user_was_online = True
            self.bot_logger.debug('Target user was already online when message was received')
            return

        self.user_was_online = False
        self.message_timestamp = time.time()
        self.last_channel_id = message.channel.id
        self.bot_logger.debug(f'Message received from {message.author} at {self.message_timestamp}')

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        """
        Handle user presence updates.

        Sends a notification message if a specific user comes online within a configured
        time window after a message was sent.

        Args:
            before (discord.Member): The member's presence state before the update.
            after (discord.Member): The member's presence state after the update.
        """
        user_id = self.bot.config.user_id
        countdown = self.bot.config.countdown

        # Add debug logging for presence changes
        if after.id == user_id:
            self.bot_logger.debug(f'User {after.name} presence changed from {before.status} to {after.status}')

        if after.id == user_id and before.status != discord.Status.online and after.status == discord.Status.online:
            if self.message_timestamp and not self.user_was_online:
                time_taken = time.time() - self.message_timestamp
                if time_taken <= countdown:
                    self.bot_logger.info(f'User {after.name} came online within {time_taken:.2f} seconds')
                    channel = self.bot.get_channel(self.last_channel_id)
                    if channel:
                        embed = discord.Embed(
                            title="🌈 Femboy Merlin ist gekommen 💦",
                            description=f"Femboy Merlin ist in nur {time_taken:.3f} Sekunden gekommen! ✨",
                            color=discord.Color.purple()
                        )
                        await channel.send(embed=embed)
                else:
                    self.bot_logger.debug(f'User {after.name} came online after {time_taken:.2f} seconds')
                self.message_timestamp = None


def setup(bot):
    """
    Add the BotEvents cog to the bot.

    Args:
        bot: The Discord bot instance.
    """
    bot.add_cog(BotEvents(bot))

from discord.ext import commands
import logging


class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_logger = logging.getLogger('bot.events')

    @commands.Cog.listener()
    async def on_ready(self):
        """Logs bot readiness and initiates archiving if enabled."""
        self.bot_logger.info(f'Logged in as {self.bot.user}')
        self.bot_logger.info('Bot ready')


def setup(bot):
    bot.add_cog(BotEvents(bot))

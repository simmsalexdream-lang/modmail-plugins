import re
from discord.ext import commands
from core import checks
from core.models import PermissionLevel

class DynamicPlaceholders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots or outside of thread channels
        if message.author.bot:
            return

        ctx = await self.bot.get_context(message)
        if not ctx.valid or not ctx.command:
            return

        # Check if we are inside an active ticket thread
        thread = await self.bot.threads.find(channel=message.channel)
        if not thread:
            return

        # Replace {0} with customer name and {1} with moderator nickname
        customer_name = thread.recipient.name
        mod_name = message.author.display_name

        if "{0}" in message.content or "{1}" in message.content:
            message.content = message.content.replace("{0}", customer_name).replace("{1}", mod_name)

async def setup(bot):
    await bot.add_cog(DynamicPlaceholders(bot))

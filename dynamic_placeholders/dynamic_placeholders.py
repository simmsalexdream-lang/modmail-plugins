from discord.ext import commands
from core import checks
from core.models import PermissionLevel

class DynamicPlaceholders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Save a reference to the original snippet expansion function
        self.original_process_snippets = bot.snippets.process_snippets

        # Inject our custom code into the bot's system
        bot.snippets.process_snippets = self.custom_process_snippets

    def cog_unload(self):
        # Restore the original function if the plugin is unloaded
        self.bot.snippets.process_snippets = self.original_process_snippets

    def custom_process_snippets(self, content, message, thread=None):
        # Run the bot's normal snippet parsing first
        content = self.original_process_snippets(content, message, thread)
        
        # If we are inside an active ticket thread, swap {0} and {1}
        if thread and thread.recipient:
            customer_name = thread.recipient.name
            mod_name = message.author.display_name
            
            if "{0}" in content:
                content = content.replace("{0}", customer_name)
            if "{1}" in content:
                content = content.replace("{1}", mod_name)
                
        return content

async def setup(bot):
    await bot.add_cog(DynamicPlaceholders(bot))

import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix=">", intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print(f"Запуск {bot.user}")

bot.load_extensions("./cogs")
# Укажите токен вашего бота здесь:
bot.run("")
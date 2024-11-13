import disnake
from disnake.ext import commands
import pyautogui
import os
import platform
import psutil
from datetime import datetime

SCREENSHOTS_FOLDER = "./screenshots"
os.makedirs(SCREENSHOTS_FOLDER, exist_ok=True)

class panelView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @disnake.ui.button(
        label="Скриншот", style=disnake.ButtonStyle.blurple, custom_id="screenshot")
    async def screenshot(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass
    
    @disnake.ui.button(
            label="Информация", style=disnake.ButtonStyle.primary, custom_id="information")
    async def information(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

    @disnake.ui.button(
        label="Выключить компьютер", style=disnake.ButtonStyle.danger, custom_id="shutdown")
    async def shutdown(self, button: disnake.ui.Button, inter:disnake.MessageInteraction):
        pass

class confirmShutdown(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Подтвердить", style=disnake.ButtonStyle.primary, custom_id="confirm")
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned)
        self.persistent_views_added = False
    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(panelView())
            self.add_view(confirmShutdown())
            self.persistent_views_added = True

class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="panel", description="Установить панель")
    async def panel(self, inter: disnake.CommandInter):

        panelEmbed = disnake.Embed(
            title="Панель управление компьютером",
            color=0x313338)
        
        view = panelView()
        await inter.send(embed=panelEmbed, view=view, ephemeral=True)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "screenshot":
            screenshot = pyautogui.screenshot()

            filename = f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            filepath = os.path.join(SCREENSHOTS_FOLDER, filename)
            screenshot.save(filepath)

            await inter.response.send_message(file=disnake.File(filepath), ephemeral=True)

        if inter.component.custom_id == "information":
            user_name = os.getlogin()
            uptime_seconds = int(psutil.boot_time())
            uptime = datetime.now() - datetime.fromtimestamp(uptime_seconds)
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            informationEmbed = disnake.Embed(
                title=f"Информация о ПК",
                color=0x313338)
            informationEmbed.add_field(name=":desktop: Общее", value=f"Имя пользователя: {user_name}\nОперационная система: {platform.system()} {platform.release()}\nВремя работы ПК: {uptime}", inline=True)
            informationEmbed.add_field(name=":bar_chart: Использование", value=f"Память: {memory.used / (1024 ** 3):.2f} ГБ / {memory.total / (1024 ** 3):.2f} ГБ ({memory.percent}%)\nДиск: {disk.used / (1024 ** 3):.2f} ГБ / {disk.total / (1024 ** 3):.2f} ГБ ({disk.percent}%)")
            
            await inter.response.send_message(embed=informationEmbed, ephemeral=True)

        if inter.component.custom_id == "shutdown":
            view = confirmShutdown()
            
            confirmEmbed = disnake.Embed(
                title="Подтверждение",
                color=0x313338)
            await inter.send(embed=confirmEmbed, view=view, ephemeral=True)
    
        if inter.component.custom_id == "confirm":
            if platform.system() == "Windows":
                os.system("shutdown /s /t 1")
            elif platform.system() == "Linux":
                os.system("shutdown now")
            else:
                await inter.send("Операционная система не поддерживается для автоматического отключения", ephemeral=True)

bot = PersistentViewBot()
def setup(bot):
    bot.add_cog(Panel(bot))
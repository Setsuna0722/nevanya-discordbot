import discord
from discord import app_commands
from config import TOKEN
from register import setup_register_command

if TOKEN is None:
    print("⚠️ Token not found!")
    exit()

# 建立 Bot
class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # 同步 Slash 指令
        await self.tree.sync()
        print("Slash 指令同步完成")

client = MyClient()
'''
# 最簡 /ping 指令
@client.tree.command(name="ping", description="測試機器人是否在線")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong 🏓")
'''
# 設定 /register 指令
setup_register_command(client)

# 啟動 Bot
client.run(TOKEN)

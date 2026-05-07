import discord
from discord import app_commands, Interaction
from discord.ui import View, Button
from google_sheet import get_players, save_result
from config import REGISTER
import time
import asyncio

# 名單快取
player_cache = {
    "data": [],
    "last_update": 0,
    "ttl": 60  # 快取 60 秒
}

async def get_cached_players():
    now = time.time()
    if now - player_cache["last_update"] > player_cache["ttl"]:
        player_cache["data"] = await asyncio.to_thread(get_players)  # list[str]
        player_cache["last_update"] = now # type: ignore
    return player_cache["data"]

# 棋盤大小選項
BOARD_SIZES = ["9路", "19路"]

register_lock = asyncio.Lock()

def setup_register_command(client):

    class ConfirmCancelView(View):
        def __init__(self, winner, loser, board_size, channel):
            super().__init__(timeout=900)
            self.winner = winner
            self.loser = loser
            self.board_size = board_size
            self.channel = channel  # 登記結果要公開的頻道

        @discord.ui.button(label="✅ 確認送出", style=discord.ButtonStyle.green) # type: ignore
        async def confirm(self, interaction: Interaction, _button: Button):
            if register_lock.locked():
                await interaction.response.send_message( # type: ignore
                    "⚠️ 尚有人在登記中，請稍後再試。",
                    ephemeral=True
                )
                return

            async with register_lock:  # 鎖定開始
                # 登記前檢查勝敗
                if self.winner == self.loser:
                    await interaction.response.send_message( # type: ignore
                        "⚠️ 勝方與敗方不能相同！",
                        ephemeral=True
                    )
                    return
                # 隱藏按鈕訊息 (先把按鈕隱藏
                await interaction.response.edit_message(view=None) # type: ignore

                # 如果你還想顯示「工作中...」，就要用 followup
                temp_msg =await interaction.followup.send("⏳ 機器人工作中...", ephemeral=True)

                # 顯示「機器人工作中...」
                #await interaction.response.defer(ephemeral=True)

                # 此為送一個暫時訊息，顯示「機器人工作中...」(不能跟隱藏按鈕共用)
                #await interaction.response.send_message("⏳ 機器人工作中...", ephemeral=True)

                # 登記資料
                result = save_result(self.winner, self.loser, self.board_size)
                registrar = interaction.user

                # 生成公開訊息
                msg = (
                    f"由  {registrar.mention}  ✅  登記成功！\n\n"
                    f"{result['number']}  {result['board_size']}\n\n"
                    f"●對局結果— {result['winner_group']}  勝  {result['loser_group']}\n\n"
                    f"●更新後分數— 賺錢組 [{result['take_money_point']}]、發財組[{result['get_rich']}]\n\n"

                    f"⬇️下一位請登記，指令 /register  —由【勝方】登記😊"
                )

                # 刪除暫時訊息
                #await interaction.delete_original_response()

                # 發送到公開頻道
                await self.channel.send(msg)

                await asyncio.sleep(5)
                await temp_msg.delete()

        @discord.ui.button(label="❌ 取消登記", style=discord.ButtonStyle.red) # type: ignore
        async def cancel(self, interaction: Interaction, _button: Button):
            await interaction.response.edit_message(content="❌ 已取消登記", view=None) # type: ignore

    @client.tree.command(name="register", description="成績登記")
    @app_commands.describe(
        winner="輸入勝方玩家名稱",
        loser="輸入敗方玩家名稱",
        board_size="選擇棋盤大小"
    )
    async def register(interaction: Interaction, winner: str, loser: str, board_size: str):
        # 限制頻道
        if interaction.channel.id != REGISTER:
            await interaction.response.send_message( # type: ignore
                "⚠️ 此指令只能在成績登記區使用", ephemeral=True
            )
            return

        # 勝敗不能相同
        if winner == loser:
            await interaction.response.send_message( # type: ignore
                "⚠️ 勝方與敗方不能相同！", ephemeral=True
            )
            return

        # 棋盤大小檢查
        if board_size not in BOARD_SIZES:
            await interaction.response.send_message( # type: ignore
                "⚠️ 請選擇正確的棋盤大小", ephemeral=True
            )
            return

        # 先 defer，避免 3 秒超時
        #await interaction.response.defer(ephemeral=True)
        players = get_players()

        # 驗證勝方
        if winner not in players:
            await interaction.response.send_message( # type: ignore
                "⚠️ 查無此勝方玩家", ephemeral=True
            )
            return
        # 驗證敗方
        if loser not in players:
            await interaction.response.send_message( # type: ignore
                "⚠️ 查無此敗方玩家", ephemeral=True
            )
            return

        # 顯示確認 / 取消按鈕（Ephemeral 給操作的人看）
        view = ConfirmCancelView(winner, loser, board_size, interaction.channel)
        await interaction.response.send_message( # type: ignore
            f"請確認以下資料：\n勝方: {winner}\n敗方: {loser}\n棋盤大小: {board_size}",
            view=view,
            ephemeral=True
        )

    # winner autocomplete
    @register.autocomplete("winner")
    async def winner_autocomplete(_interaction: Interaction, current: str):
        players = await get_cached_players()
        choices = [
            app_commands.Choice(name=p, value=p)
            for p in players if current.lower() in p.lower()
        ][:25]
        return choices

    # loser autocomplete
    @register.autocomplete("loser")
    async def loser_autocomplete(_interaction: Interaction, current: str):
        players = await get_cached_players()
        choices = [
            app_commands.Choice(name=p, value=p)
            for p in players if current.lower() in p.lower()
        ][:25]
        return choices

    # board_size autocomplete
    @register.autocomplete("board_size")
    async def board_size_autocomplete(_interaction: Interaction, current: str):
        choices = [
            app_commands.Choice(name=size, value=size)
            for size in BOARD_SIZES if current in size
        ]
        return choices

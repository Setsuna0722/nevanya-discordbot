import os
from dotenv import load_dotenv

load_dotenv()  # 將 .env 內容載入環境變數

TOKEN = os.getenv("DISCORD_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
ADMIN_ID = os.getenv("ADMIN_ID")

REGISTER = int(os.getenv("DISCORD_REGISTER_CHANNEL")) #成績登記頻道

CT_REGISTER = int(os.getenv("DISCORD_CT_REGISTER_CHANNEL")) #特定成績登記區

GOOGLE_API_KEY = os.getenv("GOOGLE_SHEET_KEY")
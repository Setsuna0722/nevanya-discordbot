import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_API_KEY

# 建立 gspread client
def get_client():
    # Google Sheet 認證
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    # 這行會讀 service_account.json
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    return gspread.authorize(creds)


def get_players():
    client_sheet = get_client()

    sheet = client_sheet.open_by_key(GOOGLE_API_KEY).worksheet("表單")

    # 取得所有玩家,去掉第一列（標題）-切片
    players = [
        name.strip()
        for name in sheet.col_values(7)[1:]
        if name.strip()
    ]

    return players

#print(get_players())

def save_result(winner, loser,board_size):
    client_sheet = get_client()
    sheet = client_sheet.open_by_key(GOOGLE_API_KEY).worksheet("成績登記表")


    #用特定某欄尋找空白列
    r_col = 18
    r_values = sheet.col_values(r_col)
    last_row = len(r_values) + 1  # 第一個空白列

    # 勝方寫入 R欄、敗方寫入 S欄、棋盤大小寫入 B欄
    sheet.update(f"R{last_row}:S{last_row}", [[winner, loser]]) # type: ignore
    sheet.update(f"B{last_row}", [[board_size]]) # type: ignore


    # 如果想抓剛寫入的這一列 A欄資料
    a_value = sheet.acell(f"A{last_row}").value  # 盤數
    c_value = sheet.acell(f"C{last_row}").value  # 勝方名稱+組別
    e_value = sheet.acell(f"E{last_row}").value  # 敗方名稱+組別
    h_value = sheet.acell(f"H{last_row}").value  # 勝方分數
    i_value = sheet.acell(f"I{last_row}").value  # 敗方分數
    l_value = sheet.acell(f"L{last_row}").value  # (賺錢)總積分
    n_value = sheet.acell(f"N{last_row}").value  # (發財)總積分

    return {
        "row": last_row,
        "winner": winner,
        "loser": loser,
        "board_size": board_size,
        "number": a_value,
        "winner_point": h_value,
        "loser_point": i_value,
        "take_money_point": l_value,
        "get_rich": n_value,
        "winner_group": c_value,
        "loser_group": e_value
    }
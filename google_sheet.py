import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

    sheet = client_sheet.open_by_key("19otSPheHkHrT7j_UEeSAUu41BxI_iu51nhdW9RDE3c4").worksheet("表單")

    # 取得所有玩家,去掉第一列（標題）-切片
    players = sheet.col_values(7)[1:]

    return players

#print(get_players())

def save_result(winner, loser):
    client_sheet = get_client()
    sheet = client_sheet.open_by_key("19otSPheHkHrT7j_UEeSAUu41BxI_iu51nhdW9RDE3c4").worksheet("成績登記表")

    # 找下一個空列編號
    last_row = len(sheet.get_all_values()) + 1

    # 勝方寫入 C欄、敗方寫入 E欄
    sheet.update(f"C{last_row}", winner)
    sheet.update(f"E{last_row}", loser)

    # 如果想抓剛寫入的這一列 A欄資料
    a_value = sheet.acell(f"A{last_row}").value  # 盤數
    b_value = sheet.acell(f"B{last_row}").value  # 棋盤大小
    h_value = sheet.acell(f"H{last_row}").value  # 勝方分數
    i_value = sheet.acell(f"I{last_row}").value  # 敗方分數
    l_value = sheet.acell(f"L{last_row}").value  # (賺錢)積分
    n_value = sheet.acell(f"N{last_row}").value  # (發財)積分
    o_value = sheet.acell(f"O{last_row}").value  # 總積分

    return {
        "row": last_row,
        "winner": winner,
        "loser": loser,
        "plate": b_value,
        "number": a_value,
        "winner_point": h_value,
        "loser_point": i_value,
        "take_money_point": l_value,
        "get_rich": n_value,
        "total_point": o_value
    }
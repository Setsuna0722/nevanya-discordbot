from google_sheet import get_client, GOOGLE_API_KEY

def get_profile_sheet():
    client = get_client()
    return client.open_by_key(GOOGLE_API_KEY).worksheet("表單")


def get_player_profile(name):
    sheet = get_profile_sheet()
    rows = sheet.get_all_records()

    for row in rows:
        if row.get("參賽暱稱", "").strip() == name:
            return {
                "name": name,
                "總盤數": row.get("19+9總盤數"),
                "勝盤數": row.get("勝盤數"),
                "敗盤數": row.get("敗盤數"),
                "個人總積分": row.get("個人積分")
            }

    return None


def get_match_sheet():
    client = get_client()
    return client.open_by_key(GOOGLE_API_KEY).worksheet("成績登記表")

def norm(x):
    return str(x).strip()


def get_player_history(name):
    sheet = get_match_sheet()
    rows = sheet.get_all_records()

    history = []

    for row in rows:

        winner = row.get("DC寫入用(勝方)")
        loser = row.get("DC寫入用(敗方)")

        # 勝場
        if norm(winner).startswith(name):
            history.append({
                "盤數": row.get("盤數").strip(),
                "棋盤大小": row.get("棋盤大小").strip(),
                "對手": loser,
                "對局結果": "Win",
                "取得積分": row.get("勝方分數"),
            })

        # 敗場
        if norm(loser).startswith(name):
            history.append({
                "盤數": row.get("盤數").strip(),
                "棋盤大小": row.get("棋盤大小").strip(),
                "對手": winner,
                "對局結果": "Lose",
                "取得積分": row.get("敗方分數")

            })
    #  print("=== DEBUG ROWS ===")
    #  print(rows[:3])
    #  print("=== CHECK NAME ===", name)
    return history


def get_player_full_data(name):

    profile = get_player_profile(name)
    history = get_player_history(name)

    return {
        "profile": profile,
        "history": history
    }
from google_sheet import get_client, GOOGLE_API_KEY
from collections import defaultdict

def get_match_rows():
    client = get_client()
    sheet = client.open_by_key(GOOGLE_API_KEY).worksheet("成績登記表")

    rows = sheet.get_all_values()
    headers = rows[0]
    data_rows = rows[1:]

    return [dict(zip(headers, r)) for r in data_rows]


#玩家統計
def build_player_stats():
    rows = get_match_rows()

    stats = defaultdict(lambda: {
        "參賽暱稱": "",
        "勝場盤數": 0,
        "敗場盤數": 0,
        "個人總積分": 0
    })

    for r in rows:

        winner = str(r.get("DC寫入用(勝方)", "")).strip()
        loser = str(r.get("DC寫入用(敗方)", "")).strip()

        win_score = r.get("勝方分數") or 0
        lose_score = r.get("敗方分數") or 0

        # winner
        if winner:
            stats[winner]["參賽暱稱"] = winner
            stats[winner]["勝場盤數"] += 1
            stats[winner]["個人總積分"] += int(win_score)

        # loser
        if loser:
            stats[loser]["參賽暱稱"] = loser
            stats[loser]["敗場盤數"] += 1
            stats[loser]["個人總積分"] += int(lose_score)

    return list(stats.values())

#總排行榜
def get_rank():
    players = build_player_stats()

    return sorted(
        players,
        key=lambda x: x["個人總積分"],
        reverse=True
    )

#分組排行榜
def get_group_rank():
    rows = get_match_rows()

    groups = {}

    def add(group, name, score):
        if group not in groups:
            groups[group] = {}

        if name not in groups[group]:
            groups[group][name] = {
                "參賽暱稱": name,
                "個人總積分": 0,
                # "勝場盤數": 0,
                # "敗場盤數": 0
            }

        groups[group][name]["個人總積分"] += score

    for r in rows:

        winner = str(r.get("DC寫入用(勝方)", "")).strip()
        loser = str(r.get("DC寫入用(敗方)", "")).strip()

        win_group = r.get("勝方組別", "未知")
        lose_group = r.get("敗方組別", "未知")

        win_score = int(r.get("勝方分數") or 0)
        lose_score = int(r.get("敗方分數") or 0)

        if winner:
            add(win_group, winner, win_score)

        if loser:
            add(lose_group, loser, lose_score)

    # convert to sorted output
    result = {}

    for g, players in groups.items():
        result[g] = sorted(players.values(), key=lambda x: x["個人總積分"], reverse=True)

    return result
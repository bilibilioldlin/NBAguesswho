import random
import utils.dataUtils as dataUtils

# 位置分组
Positions = ["PG", "SG", "SF", "PF", "C"]
PositionNames = {
    "PG": "控球后卫",
    "SG": "得分后卫",
    "SF": "小前锋",
    "PF": "大前锋",
    "C": "中锋"
}

# 联盟分区
Conferences = ["东部", "西部"]

# 难度等级标签(对应不同的子集)
Labels = [
    {"id": "random", "name": "随机", "weight": 40},
    {"id": "allstar", "name": "全明星", "weight": 25},
    {"id": "mvp", "name": "MVP", "weight": 15},
    {"id": "champion", "name": "总冠军", "weight": 20}
]


def LoadPlayerList():
    """加载并缓存球员列表"""
    return dataUtils.NbaPlayerGetter()


def OnlyNameGet(PlayerList):
    """提取所有球员名字"""
    NameList = []
    for x in PlayerList:
        NameList.append(x["name"])
    return NameList


def getPlayerByName(PlayerList, name):
    """根据姓名查找球员索引"""
    i = 0
    for x in PlayerList:
        if x["name"] == name:
            return i
        i += 1
    return None


def getPlayerByIndex(PlayerList, index_str):
    """根据index查找球员索引"""
    try:
        idx = int(index_str)
        for i, x in enumerate(PlayerList):
            if int(x["index"]) == idx:
                return i
    except (ValueError, KeyError):
        pass
    return None


def getPlayerByDf(PlayerList, hard=0, ngen=0):
    """根据难度和世代筛选一个随机球员"""
    candidates = []
    for p in PlayerList:
        if _match_hard(p, hard):
            candidates.append(p["name"])

    if not candidates:
        return random.randint(0, len(PlayerList) - 1)
    name = random.choice(candidates)
    return getPlayerByName(PlayerList, name)


def _match_hard(player, hard):
    """根据难度匹配球员"""
    if hard == 0:  # 新手模式 - MVP传奇
        return player["mvp"] >= 1
    elif hard == 1:  # 简单模式 - 总冠军球员
        return player["champion"] >= 1
    elif hard == 2:  # 普通模式 - 全明星球员
        return player["all_star"] >= 1
    elif hard == 3:  # 困难模式 - 角色球员（无全明星）
        return player["all_star"] == 0
    elif hard == 4:  # 老球迷模式 - 全部球员
        return True
    return True


def ComparePlayer(PlayerList, ans_id, guess_id):
    """比较两个球员的属性，返回给前端展示"""
    ans = PlayerList[ans_id]
    guess = PlayerList[guess_id]

    result = {"name": guess["name"]}
    result["answer"] = "True" if ans["name"] == guess["name"] else "False"
    result["index"] = guess["index"]

    # 1. 球队对比（每个球队单独匹配）
    ans_teams = set(ans.get("teams", [ans["team"]]))
    guess_teams = guess.get("teams", [guess["team"]])
    team_list = []
    for t in guess_teams:
        team_list.append({
            "name": t,
            "match": t in ans_teams
        })
    result["team"] = {
        "teams": team_list,
        "value": "True" if any(t["match"] for t in team_list) else "False"
    }

    # 2. 位置对比
    result["position"] = {
        "key": guess["positionName"],
        "value": "True" if ans["position"] == guess["position"] else "False"
    }

    # 3. 球衣号码
    num1, num2 = ans["number"], guess["number"]
    if num1 == num2:
        result["number"] = {"key": num2, "value": "equiv"}
    elif num2 > num1:
        result["number"] = {"key": num2, "value": "high"}
    else:
        result["number"] = {"key": num2, "value": "low"}

    # 4. 身高
    h1, h2 = ans["height"], guess["height"]
    if h1 == h2:
        result["height"] = {"key": h2, "value": "equiv"}
        result["height"]["dis"] = "equiv"
    elif h2 > h1:
        result["height"] = {"key": h2, "value": "high"}
        result["height"]["dis"] = "near" if abs(h2 - h1) <= 5 else "far"
    else:
        result["height"] = {"key": h2, "value": "low"}
        result["height"]["dis"] = "near" if abs(h2 - h1) <= 5 else "far"

    # 5. 体重
    w1, w2 = ans["weight"], guess["weight"]
    if w1 == w2:
        result["weight"] = {"key": w2, "value": "equiv"}
        result["weight"]["dis"] = "equiv"
    elif w2 > w1:
        result["weight"] = {"key": w2, "value": "high"}
        result["weight"]["dis"] = "near" if abs(w2 - w1) <= 8 else "far"
    else:
        result["weight"] = {"key": w2, "value": "low"}
        result["weight"]["dis"] = "near" if abs(w2 - w1) <= 8 else "far"

    # 6. 出生年份
    by1, by2 = ans["birthYear"], guess["birthYear"]
    if by1 == by2:
        result["birthYear"] = {"key": by2, "value": "equiv"}
    elif by2 > by1:
        result["birthYear"] = {"key": by2, "value": "high"}
    else:
        result["birthYear"] = {"key": by2, "value": "low"}
    if by1 == by2:
        result["birthYear"]["dis"] = "equiv"
    else:
        result["birthYear"]["dis"] = "near" if abs(by2 - by1) <= 5 else "far"

    # 7. 选秀年份
    dy1, dy2 = ans["draftYear"], guess["draftYear"]
    if dy1 == dy2:
        result["draftYear"] = {"key": dy2, "value": "equiv"}
    elif dy2 > dy1:
        result["draftYear"] = {"key": dy2, "value": "high"}
    else:
        result["draftYear"] = {"key": dy2, "value": "low"}
    if dy1 == dy2:
        result["draftYear"]["dis"] = "equiv"
    else:
        result["draftYear"]["dis"] = "near" if abs(dy2 - dy1) <= 5 else "far"

    # 8. 场均得分
    p1, p2 = ans["ppg"], guess["ppg"]
    if p1 == p2:
        result["ppg"] = {"key": p2, "value": "equiv"}
    elif p2 > p1:
        result["ppg"] = {"key": p2, "value": "high"}
    else:
        result["ppg"] = {"key": p2, "value": "low"}
    if p1 == p2:
        result["ppg"]["dis"] = "equiv"
    else:
        result["ppg"]["dis"] = "near" if abs(p2 - p1) <= 3 else "far"

    # 9. 场均篮板
    r1, r2 = ans["rpg"], guess["rpg"]
    if r1 == r2:
        result["rpg"] = {"key": r2, "value": "equiv"}
    elif r2 > r1:
        result["rpg"] = {"key": r2, "value": "high"}
    else:
        result["rpg"] = {"key": r2, "value": "low"}
    if r1 == r2:
        result["rpg"]["dis"] = "equiv"
    else:
        result["rpg"]["dis"] = "near" if abs(r2 - r1) <= 2 else "far"

    # 10. 场均助攻
    a1, a2 = ans["apg"], guess["apg"]
    if a1 == a2:
        result["apg"] = {"key": a2, "value": "equiv"}
    elif a2 > a1:
        result["apg"] = {"key": a2, "value": "high"}
    else:
        result["apg"] = {"key": a2, "value": "low"}
    if a1 == a2:
        result["apg"]["dis"] = "equiv"
    else:
        result["apg"]["dis"] = "near" if abs(a2 - a1) <= 1.5 else "far"

    # 11. 三分命中率
    t1, t2 = ans["three_pct"], guess["three_pct"]
    if t1 == t2:
        result["three_pct"] = {"key": t2, "value": "equiv"}
    elif t2 > t1:
        result["three_pct"] = {"key": t2, "value": "high"}
    else:
        result["three_pct"] = {"key": t2, "value": "low"}
    if t1 == t2:
        result["three_pct"]["dis"] = "equiv"
    else:
        result["three_pct"]["dis"] = "near" if abs(t2 - t1) <= 3 else "far"

    # 12. 全明星次数
    s1, s2 = ans["all_star"], guess["all_star"]
    if s1 == s2:
        result["all_star"] = {"key": s2, "value": "equiv"}
    elif s2 > s1:
        result["all_star"] = {"key": s2, "value": "high"}
    else:
        result["all_star"] = {"key": s2, "value": "low"}

    # 13. 总冠军
    c1, c2 = ans["champion"], guess["champion"]
    if c1 == c2:
        result["champion"] = {"key": c2, "value": "equiv"}
    elif c2 > c1:
        result["champion"] = {"key": c2, "value": "high"}
    else:
        result["champion"] = {"key": c2, "value": "low"}

    # 14. 联盟分区
    result["conference"] = {
        "key": guess["conference"],
        "value": "True" if ans["conference"] == guess["conference"] else "False"
    }

    # 15. 国家
    result["country"] = {
        "key": guess["country"],
        "value": "True" if ans["country"] == guess["country"] else "False"
    }

    return result

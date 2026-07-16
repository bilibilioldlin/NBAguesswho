import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root = current_dir + "/.."


def NbaPlayerGetter():
    """加载NBA球员列表"""
    with open(root + '/data/nba/nba_players_300.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def SrcPath():
    return root

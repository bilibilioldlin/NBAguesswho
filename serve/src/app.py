from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import utils.pokeUtils as pokeUtils

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

# 全局加载NBA球员列表
PlayerList = pokeUtils.LoadPlayerList()
NameList = pokeUtils.OnlyNameGet(PlayerList)
print(f"已加载 {len(PlayerList)} 名NBA球员")


@app.route('/debug', methods=["GET"])
def debug():
    return "NBA Guess - debug ok"


@app.route('/api/initget', methods=["GET"])
def initget():
    """根据难度初始化一局游戏，返回答案球员的index"""
    hard = request.args.get('difficulty', default=0, type=int)
    gen = request.args.get('gen', default=0, type=int)
    answer_id = pokeUtils.getPlayerByDf(PlayerList, hard, gen)
    return jsonify({"answerId": answer_id})


@app.route('/api/nameget', methods=["GET"])
def nameget():
    """获取所有球员名字列表，用于前端下拉选择"""
    return jsonify(NameList)


@app.route('/api/guess', methods=["GET"])
def guess():
    """比较猜测与答案的属性"""
    answer_id = request.args.get('answer', default=0, type=int)
    guess_name = request.args.get('guess', default='', type=str)
    guess_id = pokeUtils.getPlayerByName(PlayerList, guess_name)
    if guess_id is None:
        return jsonify({"error": "球员名不存在"}), 400
    if answer_id < 0 or answer_id >= len(PlayerList):
        return jsonify({"error": "答案ID错误"}), 400
    ans = pokeUtils.ComparePlayer(PlayerList, answer_id, guess_id)
    return jsonify(ans)


@app.route('/api/getanswer', methods=["GET"])
def getanswer():
    """获取指定答案的完整数据(用于揭晓答案)"""
    player_id = request.args.get('pokemon', default=0, type=int)
    if player_id < 0 or player_id >= len(PlayerList):
        return jsonify({"error": "球员ID错误"}), 400
    return jsonify(PlayerList[player_id])


@app.route('/api/players', methods=["GET"])
def get_players():
    """获取所有球员的完整数据(用于管理/展示)"""
    return jsonify(PlayerList)


# ============== 前端静态文件服务 ==============
@app.route('/')
def index():
    return send_from_directory("dist", "index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)

// NBA球员属性对比逻辑（从Python转换）

/**
 * 根据姓名查找球员索引
 */
export function getPlayerByName(playerList, name) {
  for (let i = 0; i < playerList.length; i++) {
    if (playerList[i].name === name) return i;
  }
  return null;
}

/**
 * 根据难度筛选一个随机球员
 */
export function getPlayerByDf(playerList, hard = 0) {
  const candidates = [];
  for (const p of playerList) {
    if (matchHard(p, hard)) {
      candidates.push(p.name);
    }
  }

  if (candidates.length === 0) {
    return Math.floor(Math.random() * playerList.length);
  }

  const name = candidates[Math.floor(Math.random() * candidates.length)];
  return getPlayerByName(playerList, name);
}

/**
 * 根据难度匹配球员
 */
function matchHard(player, hard) {
  if (hard === 0) return player.mvp >= 1;          // 新手模式 - MVP传奇
  if (hard === 1) return player.champion >= 1;     // 简单模式 - 总冠军
  if (hard === 2) return player.all_star >= 1;     // 普通模式 - 全明星
  if (hard === 3) return player.all_star === 0;    // 困难模式 - 角色球员
  if (hard === 4) return true;                     // 老球迷模式 - 全部球员
  return true;
}

/**
 * 比较两个球员的属性，返回给前端展示
 */
export function comparePlayer(playerList, ansId, guessId) {
  const ans = playerList[ansId];
  const guess = playerList[guessId];

  const result = { name: guess.name };
  result.answer = ans.name === guess.name ? "True" : "False";
  result.index = guess.index;

  // 1. 球队对比（每个球队单独匹配）
  const ansTeams = new Set(ans.teams || [ans.team]);
  const guessTeams = guess.teams || [guess.team];
  const teamList = guessTeams.map(t => ({
    name: t,
    match: ansTeams.has(t)
  }));
  result.team = {
    teams: teamList,
    value: teamList.some(t => t.match) ? "True" : "False"
  };

  // 2. 位置对比
  result.position = {
    key: guess.positionName,
    value: ans.position === guess.position ? "True" : "False"
  };

  // 3. 球衣号码
  result.number = compareNumber(ans.number, guess.number);

  // 4. 身高
  result.height = compareWithDis(ans.height, guess.height, 5);

  // 5. 体重
  result.weight = compareWithDis(ans.weight, guess.weight, 8);

  // 6. 出生年份
  result.birthYear = compareWithDis(ans.birthYear, guess.birthYear, 5);

  // 7. 选秀年份
  result.draftYear = compareWithDis(ans.draftYear, guess.draftYear, 5);

  // 8. 场均得分
  result.ppg = compareWithDis(ans.ppg, guess.ppg, 3);

  // 9. 场均篮板
  result.rpg = compareWithDis(ans.rpg, guess.rpg, 2);

  // 10. 场均助攻
  result.apg = compareWithDis(ans.apg, guess.apg, 1.5);

  // 11. 三分命中率
  result.three_pct = compareWithDis(ans.three_pct, guess.three_pct, 3);

  // 12. 全明星次数
  result.all_star = compareNumber(ans.all_star, guess.all_star);

  // 13. 总冠军
  result.champion = compareNumber(ans.champion, guess.champion);

  // 14. 联盟分区
  result.conference = {
    key: guess.conference,
    value: ans.conference === guess.conference ? "True" : "False"
  };

  // 15. 国家
  result.country = {
    key: guess.country,
    value: ans.country === guess.country ? "True" : "False"
  };

  return result;
}

/**
 * 比较数值（无距离判断）
 */
function compareNumber(ans, guess) {
  if (ans === guess) return { key: guess, value: "equiv" };
  if (guess > ans) return { key: guess, value: "high" };
  return { key: guess, value: "low" };
}

/**
 * 比较数值（带距离判断）
 */
function compareWithDis(ans, guess, nearThreshold) {
  if (ans === guess) {
    return { key: guess, value: "equiv", dis: "equiv" };
  }
  if (guess > ans) {
    return {
      key: guess,
      value: "high",
      dis: Math.abs(guess - ans) <= nearThreshold ? "near" : "far"
    };
  }
  return {
    key: guess,
    value: "low",
    dis: Math.abs(guess - ans) <= nearThreshold ? "near" : "far"
  };
}

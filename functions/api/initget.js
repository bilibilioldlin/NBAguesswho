// GET /api/initget - 根据难度初始化游戏
import { PlayerList } from './_lib/nbaData.js';
import { getPlayerByDf } from './_lib/pokeUtils.js';

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const difficulty = parseInt(url.searchParams.get('difficulty') || '0');

  const answerId = getPlayerByDf(PlayerList, difficulty);

  return new Response(JSON.stringify({ answerId }), {
    headers: { 'Content-Type': 'application/json' }
  });
}

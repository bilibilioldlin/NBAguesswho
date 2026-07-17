// GET /api/getanswer - 获取指定答案的完整数据（用于揭晓答案）
import { PlayerList } from './_lib/nbaData.js';

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const playerId = parseInt(url.searchParams.get('player') || '0');

  if (playerId < 0 || playerId >= PlayerList.length) {
    return new Response(JSON.stringify({ error: '球员ID错误' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  return new Response(JSON.stringify(PlayerList[playerId]), {
    headers: { 'Content-Type': 'application/json' }
  });
}

// GET /api/players - 获取所有球员的完整数据
import { PlayerList } from './_lib/nbaData.js';

export async function onRequestGet(context) {
  return new Response(JSON.stringify(PlayerList), {
    headers: { 'Content-Type': 'application/json' }
  });
}

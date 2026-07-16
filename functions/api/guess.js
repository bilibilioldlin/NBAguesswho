// GET /api/guess - 比较猜测与答案的属性
import { PlayerList } from './_lib/nbaData.js';
import { getPlayerByName, comparePlayer } from './_lib/pokeUtils.js';

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const answerId = parseInt(url.searchParams.get('answer') || '0');
  const guessName = url.searchParams.get('guess') || '';

  const guessId = getPlayerByName(PlayerList, guessName);
  if (guessId === null) {
    return new Response(JSON.stringify({ error: '球员名不存在' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  if (answerId < 0 || answerId >= PlayerList.length) {
    return new Response(JSON.stringify({ error: '答案ID错误' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  const result = comparePlayer(PlayerList, answerId, guessId);
  return new Response(JSON.stringify(result), {
    headers: { 'Content-Type': 'application/json' }
  });
}

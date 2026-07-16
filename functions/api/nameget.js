// GET /api/nameget - 获取所有球员名字列表
import { NameList } from './_lib/nbaData.js';

export async function onRequestGet(context) {
  return new Response(JSON.stringify(NameList), {
    headers: { 'Content-Type': 'application/json' }
  });
}

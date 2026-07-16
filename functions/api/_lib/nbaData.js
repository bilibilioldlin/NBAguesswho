// NBA球员数据加载模块
import playerData from '../../../data/nba/nba_players_300.json';

// 缓存球员列表
const PlayerList = playerData;

// 缓存名字列表
const NameList = PlayerList.map(p => p.name);

export { PlayerList, NameList };

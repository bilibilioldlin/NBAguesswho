import json
import os

data_dir = r"D:\desktop\2026.7.16\pokemonle-main\data\nba"

# 读取现有数据
with open(os.path.join(data_dir, 'nba_players_300.json'), 'r', encoding='utf-8-sig') as f:
    all_players = json.load(f)
print(f'现有球员数: {len(all_players)}')

# 读取5个批次
batches = ['batch1.json', 'batch2.json', 'batch3.json', 'batch4.json', 'batch5.json']
new_count = 0
for batch in batches:
    with open(os.path.join(data_dir, batch), 'r', encoding='utf-8-sig') as f:
        batch_data = json.load(f)
    all_players.extend(batch_data)
    new_count += len(batch_data)
    print(f'{batch}: {len(batch_data)}人')

print(f'合并后总数: {len(all_players)}人')

# 去重（按名字）
seen_names = set()
unique_data = []
duplicates = []
for player in all_players:
    if player['name'] not in seen_names:
        seen_names.add(player['name'])
        unique_data.append(player)
    else:
        duplicates.append(player['name'])

print(f'重复人数: {len(duplicates)}人')
if duplicates:
    print(f'重复名单: {duplicates}')

print(f'去重后总数: {len(unique_data)}人')
print(f'实际新增: {len(unique_data) - 300}人')

# 更新index
for i, player in enumerate(unique_data, 1):
    player['index'] = f'{i:04d}'

# 写入新文件
with open(os.path.join(data_dir, 'nba_players_300.json'), 'w', encoding='utf-8') as f:
    json.dump(unique_data, f, ensure_ascii=False, indent=2)

print('已完成合并！')
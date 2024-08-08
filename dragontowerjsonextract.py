import json
import os

current_dir = os.getcwd()

# change the filename here to desired filename.
file_path = os.path.join(current_dir, 'archive_2024-07-26.json')

with open(file_path, 'r') as file:
    json_data = file.read()

data_list = json.loads(json_data)

if data_list:
    first_data = data_list[0]
    timestamp = first_data['created_at']
    print(f"Timestamp: {timestamp}")
    print() 


for data in data_list:

    if data['data']['gameType'] == 'Dragon Tower':
        house_id = data['data']['iid']
        client_seed = data['data']['clientSeed']
        server_seed_hash = data['data']['serverSeedHash']
        difficulty = data['data']['stateDragonTower']['difficulty']
        rounds = data['data']['stateDragonTower']['_rounds']
        nonce = data['data']['nonce']
        tiles_selected = data['data']['stateDragonTower']['tilesSelected']


        print("Bet ID:", house_id, "Link: https://stake.us/casino/games/dragon-tower?iid=" + house_id + "&modal=bet")
        print("HMAC:", client_seed, ":", server_seed_hash, ":", nonce)
        print("Nonce:", nonce)
        print("Difficulty:", difficulty)
        print()
        print("Rounds:", rounds)
        print("Tiles Selected:", tiles_selected)
        print()  

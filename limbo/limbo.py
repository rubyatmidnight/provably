import hmac
import hashlib
import csv

# implementation

def byte_generator(server_seed, client_seed, nonce):
    current_round = 0

    while True:
        hmac_obj = hmac.new(server_seed, f"{client_seed}:{nonce}:{current_round}".encode(), hashlib.sha256)
        buffer = hmac_obj.digest()

        for byte in buffer:
            yield byte

        current_round += 1

# conversion 

def generate_floats(server_seed, client_seed, nonce, count):
    rng = byte_generator(server_seed, client_seed, nonce)

    bytes_list = []

    for _ in range(count * 4):
        bytes_list.extend(next(rng) for _ in range(4))

    floats = []
    for i in range(0, len(bytes_list), 4):
        byte_chunk = bytes_list[i:i+4]
        value = sum(byte * 256**(3-j) for j, byte in enumerate(byte_chunk))
        floats.append(value / 2**32)

    return floats

# game event

def calculate_result(float_value, house_edge=0.99):
    float_point = 1e8 / ((float_value * 1e8) / house_edge)
    crash_point = int(float_point * 100) / 100
    result = max(crash_point, 1)
    return result

server_seed = b"685986833f1bc1e3b9a987cc8c703f63ca742c8992d41fe70682b3ba0e176d09"
client_seed = r'''06f0b3a99444987137e24524356210cf1cb324cb0033c36ecd6e7cc5afb5c8b5'''
nonce_count = 50000

print(server_seed)
print(client_seed)

# function done, export to csv

with open('limboresults.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Nonce', 'Result']) 

    for nonce in range(nonce_count):
        floats = generate_floats(server_seed, client_seed, nonce, 1)
        final_result = calculate_result(floats[0])
        writer.writerow([nonce, final_result]) 
        print(f"Nonce: {nonce}, Final Result: {final_result}")
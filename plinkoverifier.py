import hmac
import hashlib
import csv
import os

def byte_generator(server_seed, client_seed, nonce, cursor):
    current_round = cursor // 32
    current_round_cursor = cursor % 32
    while True:
        message = f"{client_seed}:{nonce}:{current_round}".encode()
        hmac_digest = hmac.new(server_seed.encode(), message, hashlib.sha256).digest()
        while current_round_cursor < 32:
            yield hmac_digest[current_round_cursor]
            current_round_cursor += 1
        current_round_cursor = 0
        current_round += 1

def generate_floats(server_seed, client_seed, nonce, cursor, count):
    rng = byte_generator(server_seed, client_seed, nonce, cursor)
    bytes_list = []
    for _ in range(count * 4):
        bytes_list.append(next(rng))
    floats = []
    for byte_chunk in [bytes_list[i:i+4] for i in range(0, len(bytes_list), 4)]:
        value = sum(byte / 256**(i+1) for i, byte in enumerate(byte_chunk))
        floats.append(value)
    return floats

def plinko_event(float_value):
    if float_value * 2 < 1:
        return 0  # left
    else:
        return 1  # right

def get_plinko_result(server_seed, client_seed, nonce, cursor):
    floats = generate_floats(server_seed, client_seed, nonce, cursor, rows)
    result = sum(plinko_event(float_value) for float_value in floats)
    return result

def generate_plinko_results_csv(server_seed, client_seed, nonce_start, nonce_end, cursor, output_file):
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Nonce', 'Plinko Result'])
            for nonce in range(nonce_start, nonce_end):
                plinko_result = get_plinko_result(server_seed, client_seed, nonce, cursor)
                writer.writerow([nonce, plinko_result])

    except PermissionError:
        print(f"Write error, creating new csv file.")
        base_filename, ext = os.path.splitext(output_file)
        new_filename = f"{base_filename}_new{ext}"
        with open(new_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Nonce', 'Plinko Result'])
            for nonce in range(nonce_start, nonce_end):
                plinko_result = get_plinko_result(server_seed, client_seed, nonce, cursor)
                writer.writerow([nonce, plinko_result])


server_seed = input("Enter unhashed server seed...: ")
client_seed = input("Enter client seed...: ")
nonce_start = 0
nonce_end = int(input("Enter desired end nonce as an integer: "))
rows = int(input("Insert desired rows: "))
cursor = 0
output_file = 'plinkoresults.csv'
generate_plinko_results_csv(server_seed, client_seed, nonce_start, nonce_end, cursor, output_file)
print(f"Plinko results have been written to {output_file}")

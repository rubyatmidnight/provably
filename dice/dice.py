import hashlib
from hmac import HMAC
import math
import csv
import os

def byteGenerator(serverSeed, clientSeed, nonce, cursor=0):
    """Random number generation based on serverSeed, clientSeed, nonce and cursor"""
    currentRound = 0
    currentRoundCursor = cursor

    while True:
        # hmac generation is the core of the rng process of the implementation
        hmac = HMAC(serverSeed.encode(), f"{clientSeed}:{nonce}:{currentRound}".encode(), hashlib.sha256)
        buffer = hmac.digest()

        # while the cursor function is included. dice does not use a round cursor higher than 0. if this script were adapted to another game this may be useful. 
        while currentRoundCursor < 32:
            yield buffer[currentRoundCursor]
            currentRoundCursor += 1

        currentRoundCursor = 0
        currentRound += 1

def generateFloats(serverSeed, clientSeed, nonce, cursor=0, count=1):
    # convert the hash output from the byteGenerator to floats
    rng = byteGenerator(serverSeed, clientSeed, nonce, cursor)
    bytes = []

    # this sets up the game event with the implementation of the rng
    while len(bytes) < count * 4:
        bytes.append(next(rng))

    # floats are used in the game event
    floats = []
    for bytesChunk in [bytes[i:i+4] for i in range(0, len(bytes), 4)]:
        result = 0
        for i, value in enumerate(bytesChunk):
            divider = 256 ** (i + 1)
            partialResult = value / divider
            result += partialResult
        floats.append(result)

    return floats

def diceRoll(float):
    # game event translation
    scaled_value = (float * 10001) / 100  # Multiply by 100 to get 2 decimal places
    rounded_down = math.floor(scaled_value * 100) / 100  # Round down and then divide by 100 to get 2 decimal places
    return rounded_down

def verify(clientSeed, serverSeed, nonce_start, nonce_end, output_file):

    # generates game events; each event is a roll. we can roll as many of these as desired. 
    results = []
    for nonce in range(nonce_start, nonce_end + 1):
        floats = generateFloats(serverSeed, clientSeed, str(nonce))
        rolls = [diceRoll(float) for float in floats]
        for roll in rolls:
            results.append([nonce, roll])

    # writing the rolls to csv files
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Nonce', 'Roll','', 'Unhashed Server Seed:'+ serverSeed, 'Client Seed:' + clientSeed])
            writer.writerows(results)
    except PermissionError:
        print(f"Error: Unable to write to {output_file}. Creating a new file.")
        base_filename, ext = os.path.splitext(output_file)
        new_filename = f"{base_filename}_new{ext}"
        with open(new_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Nonce', 'Roll','', 'Unhashed Server Seed:'+ serverSeed, 'Client Seed:' + clientSeed])
            writer.writerows(results)
        print(f"Results written to {new_filename}")


# variables. for posterity I am including the sha256 encoder so that if something is incorrect, it will tell the user. 
# possible issues: if the user has special characters in their client seed, it may not work. that would require forcing a literal interpretation of the string. this is probably not hard to do but i didnt do it now.
# if you need to do this and the values are not matching up to corroborating evidence, change that to (exactly like the below) and remove the hashtag.
# clientSeed = '''clientseed'''
hserverSeed = input("Enter hashed server seed...")
serverSeed = input("Enter unhashed server seed...")
clientSeed = input("Enter client seed...")
# if desired, you can change the nonce start so that you can generate from a particular point. by default I am leaving it at 0
nonce_start = 0
nonce_end = int(input("Enter last nonce to count..."))
output_file = "rolls.csv"

# input both strings. they must be sha256, not sha512. 

def sha256_encode(data):
    # this will check if serverSeed is able to be resolved as hserverSeed. If it does, then you were not given a false server seed at any point. 
    return hashlib.sha256(data.encode()).hexdigest()

hashed_input = sha256_encode(serverSeed)

provided_hashed_result = hserverSeed

print("Encoded Server Seed:", hashed_input)
print("Provided hashed result:", provided_hashed_result)

if hashed_input == provided_hashed_result:
    print("Hashes match.")
else:
    print("Hashes do not match, please ensure these are the correct inputs.")
    resolution = input("Do you still want to proceed with generating rolls? (Y/N): ")
    if resolution != "Y":
        exit()
    else:
        verify(clientSeed, serverSeed, nonce_start, nonce_end, output_file)
        print("Finished, .csv file output to folder.")

    

# and then the function proceeds.
verify(clientSeed, serverSeed, nonce_start, nonce_end, output_file)
print("Finished, .csv file output to folder.")
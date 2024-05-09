import random

symbols = ['u', 'o', '♡']
probabilities = [0.5, 0.3, 0.1]
balance = 1000

def spin():
    ## select for 1 and 3 position
    first_third_symbols = [random.choices(symbols, probabilities)[0] for _ in range(2)]
    
    second_symbol = random.choice(['v', 'w', '♡'])
    
    ## construct the spin result
    result = ''.join([first_third_symbols[0], second_symbol, first_third_symbols[1]])  # Join symbols into a single string
    print()
    return result

## determine winnings
def calculate_winnings(spin_result):
    ## payouts
    payouts = {'uwu': 500, 'owo': 500, 'ovo': 100, '♡w♡': 5000, '♡♡♡': 20000}
    
    spin_str = ''.join(spin_result)
    if spin_str in payouts:
        return payouts[spin_str]
    else:
        return 0

## function
def play_slot_machine():
    global balance  
    
    print("Welcome!")
    while True:
        play_again = input("Press Enter, or type 'exit' to exit: ")
        if play_again.lower() == 'exit':
            break
        
        if play_again == "":
            spin_result = spin()
            print("Result:", spin_result)
            winnings = calculate_winnings(spin_result)
            if winnings > 0:
                print()
                print("You won {} coins!".format(winnings))
                balance += winnings 
                print(balance)
            else:
                balance -= 100  
                print()
                print("Unlucky!")
                print()

play_slot_machine()

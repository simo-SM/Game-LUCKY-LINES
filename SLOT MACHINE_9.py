#  Lucky Lines - Slot Machine Game 
# Developed in Python - Simple CLI Casino Game
# Author: [Your Name]
# Description: Spin the reels, match symbols across lines, and win based on bets!

import random
import sys
import time
import os

# Game Configuration Constants
MAX_LINES = 3           # Maximum lines a player can bet on
MAX_BET = 100           # Maximum bet per line
MIN_BET = 1             # Minimum bet per line

ROWS = 3                # Slot machine rows
COLS = 3                # Slot machine columns

# Symbols with their appearance frequency
symbol_count = {
    "A": 2,     # Rare symbol (high reward)
    "B": 4,
    "C": 6,
    "D": 8      # Common symbol (low reward)
}

# Symbol payout values
symbol_value = {
    "A": 5,     # High payout
    "B": 4,
    "C": 3,
    "D": 2      # Low payout
}

# Check winnings: compares each line across all columns
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

# Generate random slot machine columns based on symbol counts
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns

# Print the slot machine with optional highlighting of winning lines
def print_slot_machine(columns, winning_lines=[]):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            symbol = column[row]
            if (row + 1) in winning_lines:
                symbol = f"*{symbol}*"  # Highlight winning symbol
            end_char = " | " if i != len(columns) - 1 else ""
            print(symbol, end=end_char)
        print()

# Ask user to deposit balance
def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a valid number.")
    return amount

# Ask user how many lines they want to bet on
def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines

# Ask user how much to bet per line
def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")
    return amount

# Handle one spin of the game
def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"Insufficient funds. Your current balance is: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)

    print_slot_machine(slots, winning_lines)
    print(f"\033[1;33mYou won ${winnings}.")
    print("Winning lines:", *winning_lines)
    return winnings - total_bet

# Entry point of the game
def main():
    balance = deposit()

    # Fancy welcome title with animation
    def jalan(z):
        for e in z + '\n':
            sys.stdout.write(e)
            sys.stdout.flush()
            time.sleep(0.00001)

    jalan("""
\033[1;34m                                                        ===========================================
\033[1;34m                                                        |         WELCOME TO LUCKY LINES!        |
\033[1;34m                                                        ===========================================

\033[1;31m                                                                ___      _     _     _            
\033[1;31m                                                               | _ ) ___| |__ (_)___| |_ ___ _ _  
\033[1;31m                                                               | _ \/ -_) '_ \| (_-<  _/ -_) '_| 
\033[1;31m                                                               |___/\___|_.__/|_/__/\__\___|_|    
""")

    while True:
        print(f"\033[1;32mCurrent balance: ${balance}")
        answer = input("\033[1;32mPress Enter to play (or type 'q' to quit): ")
        if answer.lower() == "q":
            break
        balance += spin(balance)

    print(f"\033[1;36mYou left the game with ${balance}. Thanks for playing!")

# Start the game
main()

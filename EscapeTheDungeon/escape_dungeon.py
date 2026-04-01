# escape_dungeon.py
# This file runs the main Escape the Dungeon game using imported classes

from game_utils import Player, AIEnemy, Room
import sys
import os
import pickle

SAVE_FILE = "dungeon_save.pkl"

# Save the current game state to a file
def save_game(player, ai):
    with open(SAVE_FILE, "wb") as f:
        pickle.dump((player, ai), f)
    print("Game saved.")

# Load the game state from a file (uses exception handling)
def load_game():
    try:
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return None, None

# Main game function
def main():
    # Set difficulty based on command-line argument
    difficulty = "easy"
    if len(sys.argv) > 1:
        difficulty = sys.argv[1].lower()

    print("Welcome to ESCAPE THE DUNGEON!")

    # Ask player if they want to load a previous save
    choice = input("Load previous game? (y/n): ").strip().lower()
    if choice == "y":
        player, ai = load_game()
        if not player:
            print("No saved game found. Starting new game.")
            player, ai = Player(), AIEnemy()
    else:
        player, ai = Player(), AIEnemy()

    # Set number of rooms based on difficulty
    room_limit = 5 if difficulty == "easy" else 7

    # Main gameplay loop
    while player.is_alive() and player.position <= room_limit:
        room = Room(player.position)
        room.enter(player)

        print("Which direction do you want to go next?")
        move = input("Move (N/S/E/W or save/quit): ").strip().lower()

        if move == "save":
            save_game(player, ai)
            break
        elif move == "quit":
            print("Goodbye!")
            break

        player.move(move)
        ai.update_memory(player.position)
        ai.move()

        if ai.caught_player(player.position):
            print("💀 The AI enemy has caught you! Game over.")
            return

    # End-game messages based on outcome
    if player.position > room_limit:
        print("🎉 You escaped the dungeon! Victory!")
    elif not player.is_alive():
        print("💀 You have perished in the dungeon...")

# Entry point
if __name__ == "__main__":
    main()
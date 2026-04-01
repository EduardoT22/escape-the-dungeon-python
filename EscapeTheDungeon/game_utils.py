# game_utils.py
# This file defines the Player, AIEnemy, and Room classes used in the game

import random

# Player class handles health, movement, and position
class Player:
    def __init__(self, name="Hero"):
        self.name = name
        self.health = 3
        self.position = 1

    def move(self, direction):
        # Move to the next room (simplified)
        print(f"{self.name} moves {direction}.")
        self.position += 1

    def take_damage(self):
        # Reduce health if player gets hit
        self.health -= 1
        print("You took damage! Health:", self.health)

    def is_alive(self):
        # Check if player is still alive
        return self.health > 0

# AIEnemy class follows the player and "learns" their movement pattern
class AIEnemy:
    def __init__(self):
        self.position = 0
        self.memory = []

    def update_memory(self, player_position):
        # Track recent positions (limit to 3)
        self.memory.append(player_position)
        if len(self.memory) > 3:
            self.memory.pop(0)

    def move(self):
        # Move based on most frequent recent player location
        if self.memory:
            target = max(set(self.memory), key=self.memory.count)
            self.position += 1 if self.position < target else -1
        else:
            self.position += 1

    def caught_player(self, player_position):
        # Check if AI has caught the player
        return self.position == player_position

# Room class defines events that occur when player enters a room
class Room:
    def __init__(self, number):
        self.number = number
        self.event = random.choice(["riddle", "trap", "safe", "easter"])

    def enter(self, player):
        # Display room info and trigger event
        print(f"\n--- Room {self.number} ---")
        if self.event == "riddle":
            self.riddle(player)
        elif self.event == "trap":
            self.trap(player)
        elif self.event == "easter":
            print("You found an Easter egg! +1 HP")
            player.health += 1
        else:
            print("This room is empty... for now.")

    def riddle(self, player):
        # Present a simple riddle
        print("Solve this riddle: What has to be broken before you can use it?")
        answer = input("Your answer: ").strip().lower()
        if answer != "egg":
            print("Wrong! You lose 1 health.")
            player.take_damage()
        else:
            print("Correct!")

    def trap(self, player):
        # 50% chance to trigger a trap
        if random.random() < 0.5:
            print("You triggered a trap! Lose 1 health.")
            player.take_damage()
        else:
            print("You narrowly avoided a trap.")
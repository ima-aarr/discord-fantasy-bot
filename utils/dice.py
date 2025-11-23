# utils/dice.py
import random

def d(sides=100):
    return random.randint(1, sides)

def roll(count=1, sides=6):
    return sum(random.randint(1, sides) for _ in range(count))

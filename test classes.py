import random
import math

def speed_calculator(difficulty):
    return 1 + (difficulty * 0.5)

def y_calculator(x):
    return -50  # Items start above screen

class Items:
    def __init__(self, speed, x, y, letter):
        self.speed = speed
        self.x = x
        self.y = y
        self.letter = letter
    
    def move(self):
        self.y += self.speed
    
    def is_off_screen(self, screen_height):
        return self.y > screen_height

class Fruits(Items):
    def __init__(self, speed, x, y, letter):
        super().__init__(speed, x, y, letter)
        self.points = 10
    
    def score_points(self):
        return self.points
    
    def move(self):
        super().move()  # Normal vertical movement

class Specials(Items):
    def __init__(self, speed, x, y, letter):
        super().__init__(speed, x, y, letter)
        self.power_up_duration = 5  # seconds
    
    def activate_power(self):
        return {
            'type': 'power_up',
            'duration': self.power_up_duration
        }
    
    def move(self):
        # Zigzag movement for special items
        self.y += self.speed
        self.x += math.sin(self.y/30) * 2
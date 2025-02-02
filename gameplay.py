from math import fabs
import time
import pygame
import random

# Initialisation PyGame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(2)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Window Dimension
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Display Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Slicer")

# Fruits and special objects loading
FRUIT_IMAGES = {
    "apple": pygame.image.load(r"media\img\apple.png"),
    "banana": pygame.image.load(r"media\img\banana.png"),
    "pear": pygame.image.load(r"media\img\pear.png"),
    "watermelon": pygame.image.load(r"media\img\watermelon.png"),
    "bomb": pygame.image.load(r"media\img\bomb.png"),
    "ice": pygame.image.load(r"media\img\ice.png")
}

# Background loading
BACKGROUND_IMAGE = pygame.image.load(r"media\img\background.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Explosion loading
EXPLOSION_IMAGE = pygame.image.load(r"media\img\explosion.png")

# Resize images
EXPLOSION_IMAGE = pygame.transform.scale(EXPLOSION_IMAGE, (80, 80))
for key in FRUIT_IMAGES:
    FRUIT_IMAGES[key] = pygame.transform.scale(FRUIT_IMAGES[key], (80, 80))

# Font and text
font = pygame.font.Font(None, 36)

# Sounds loading
SLICE_SOUND = pygame.mixer.Sound(r"media\sounds\slice_sound.mp3")
BOMB_SOUND = pygame.mixer.Sound(r"media\sounds\bomb_sound.mp3")
ICE_SOUND = pygame.mixer.Sound(r"media\sounds\ice_sound.mp3")
COMBO_SOUND = pygame.mixer.Sound(r"media\sounds\combo_sound.mp3")

# Class of the game
class FruitSlicerGame:
    # Initialisation
    def __init__(self, difficulty, player):
        self.last_spawn_time = 0
        self.spawn_delay = 1
        self.fruits = []
        self.explosions = []
        self.player_score = 0
        self.missed_fruits = 0
        self.game_over = False
        self.angle = 0
        self.is_frozen = False
        self.freeze_end_time = 0
        self.difficulty = difficulty
        self.player = player
        self.tuto_freeze = False

    # Function to get the fruit rates
    def get_fruit_rates(self,difficulty):
        if difficulty == 'easy':
            return 0.9
        if difficulty == 'medium':
            return 0.8
        if difficulty == 'hard':
            return 0.7
        if difficulty == 'tuto':
            return 1
        if difficulty == 'tuto_ice':
            -1
        if difficulty == 'tuto_bomb':
            -1
        return 0.9

    # Function to get the difficulty rates
    def difficulty_rates(self,difficulty):
        if difficulty == 'easy':
            return 0.05
        if difficulty == 'medium':
            return 0.04
        if difficulty == 'hard':
            return 0.03
        if difficulty == 'tuto':
            1
        return 0.05

    # Function to spawn the fruit
    def spawn_fruit(self,difficulty, count=1):
        fruit_spawn_rate = self.difficulty_rates(difficulty)
        special_spawn_rates = self.get_fruit_rates(difficulty)
        if not self.is_frozen and random.random() < fruit_spawn_rate:
            self.spawn_fruit(difficulty, count=1)
        NORMAL_FRUITS = ["apple", "banana", "pear", "watermelon"]
        SPECIAL_OBJECTS = ["bomb", "ice"]

        for _ in range(count):
            # Initial position
            spawn_x = random.randint(200, SCREEN_WIDTH - 200)
            spawn_y = SCREEN_HEIGHT - 150

            # Letter associated with the fruit
            assigned_letter = chr(random.randint(65, 90))

            # Type of fruit
            if difficulty == 'tuto_ice':
                fruit_type = SPECIAL_OBJECTS[1]
            elif difficulty == 'tuto_bomb':
                fruit_type = SPECIAL_OBJECTS[0]
            elif random.random() < special_spawn_rates:
                fruit_type = random.choice(NORMAL_FRUITS)
            else:
                fruit_type = random.choice(SPECIAL_OBJECTS)

            # Initial speed
            horizontal_speed = random.uniform(-4, 4)
            vertical_speed = random.uniform(-12, -8)
            gravity = 0.3

            # Add the fruit to the list
            self.fruits.append({
                "position_x": spawn_x,
                "position_y": spawn_y,
                "letter": assigned_letter,
                "image": FRUIT_IMAGES[fruit_type],
                "speed_x": horizontal_speed,
                "speed_y": vertical_speed,
                "gravity": gravity,
                "rotation_angle": 0,
                "rotation_speed": random.uniform(-5, 5)
            })

    def find_duplicate_letters(self):
        letter_count = {}
        for fruit in self.fruits:
            letter = fruit["letter"].lower()
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1
        return letter_count

    # Function to update the fruits
    def update_fruits(self):
        if self.is_frozen or self.tuto_freeze:
            return # Fruits no update when it's freeze

        active_fruits = [] # Fruits that are still on the screen

        for fruit in self.fruits:
            # Movement of the fruit
            fruit["position_x"] += fruit["speed_x"]
            fruit["position_y"] += fruit["speed_y"]
            fruit["speed_y"] += fruit["gravity"]

            # Rotation of the fruit
            fruit["rotation_angle"] += fruit["rotation_speed"]

            # Delete fruits that are out of the screen
            if fruit["position_y"] > SCREEN_HEIGHT + 50:
                if fruit["image"] == FRUIT_IMAGES["bomb"]:
                    pass
                else:
                    self.missed_fruits += 1
            else:
                active_fruits.append(fruit)

        self.fruits = active_fruits



    # Function to check the key press
    def check_key_press(self, key):
        remaining_fruits = []
        combo_letters = self.find_duplicate_letters()
        for fruit in self.fruits:
            if key == ord(fruit["letter"].lower()):
                letter = fruit["letter"].lower()
                if letter in combo_letters and combo_letters[letter] > 1:
                    COMBO_SOUND.play()
                    text = font.render(f"Combo! x{combo_letters[letter]}", True, BLACK)
                    screen.blit(text,(fruit["position_x"]+50, fruit["position_y"]+50))
                    self.player_score += combo_letters[letter]-1
                # If it's a bomb, the game is over
                if fruit["image"] == FRUIT_IMAGES["bomb"]:
                    BOMB_SOUND.play()
                    game_over_text = font.render("Game Over ! You sliced a bomb", True, BLACK)
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    self.game_over = True
                # If it's an ice cube, freeze the game for 4 seconds
                elif fruit["image"] == FRUIT_IMAGES["ice"]:
                    self.player_score += 10
                    ICE_SOUND.play()
                    self.is_frozen = True
                    self.tuto_freeze = False
                    self.freeze_end_time = pygame.time.get_ticks() + 4000  # Freeze for 4 seconds
                else:
                    self.player_score += 5
                    SLICE_SOUND.play()
                    # Add an explosion
                    self.explosions.append({
                        "position_x": fruit["position_x"],
                        "position_y": fruit["position_y"],
                        "start_time": pygame.time.get_ticks()
                    })

            else:
                remaining_fruits.append(fruit)
        self.fruits = remaining_fruits

    # Function to draw the fruits
    def draw_fruits(self):
        for fruit in self.fruits:
            # Rotation of the fruit
            rotated_image = pygame.transform.rotate(fruit["image"], fruit["rotation_angle"])
            new_rect = rotated_image.get_rect(center=fruit["image"].get_rect(topleft=(fruit["position_x"], fruit["position_y"])).center)

            screen.blit(rotated_image, new_rect.topleft)
            text = font.render(fruit["letter"], True, BLACK)
            screen.blit(text, (fruit["position_x"] + 25, fruit["position_y"] + 25))

        # Draw the explosions
        current_time = pygame.time.get_ticks()
        for explosion in self.explosions[:]:
            if current_time - explosion["start_time"] < 300:  # Display the explosion for 300 ms
                screen.blit(EXPLOSION_IMAGE, (explosion["position_x"], explosion["position_y"]))
            else:
                self.explosions.remove(explosion)  # Remove explosion after 300 ms

    def tuto_fruit(self):
        screen.blit(BACKGROUND_IMAGE, (0,0))
        self.spawn_fruit('tuto',1)
        self.tuto_freeze = False

        while not self.tuto_freeze:
            screen.blit(BACKGROUND_IMAGE, (0,0))
            self.update_fruits()
            self.draw_fruits()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            for fruit in self.fruits:
                if fruit["speed_y"]>0:
                    self.tuto_freeze = True
            
            pygame.display.flip()
            clock.tick(30)
            
        while self.fruits:
            screen.blit(BACKGROUND_IMAGE, (0,0))
            self.draw_fruits()
            tuto_fruit_text = font.render("Here is a fruit, Press the according letter to slash it !", True, BLACK)
            screen.blit(tuto_fruit_text, (100, 100))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    self.check_key_press(event.key)
            pygame.display.flip()
            clock.tick(30)

    def tuto_strike(self):
        self.tuto_freeze = False
        screen.blit(BACKGROUND_IMAGE, (0,0))
        self.spawn_fruit('tuto',1)

        while not self.tuto_freeze:
            screen.blit(BACKGROUND_IMAGE, (0,0))
            self.update_fruits()
            self.draw_fruits()
            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if self.missed_fruits > 1 and not self.fruits:
                tuto_strike_text = font.render("If you miss a fruit, it's going to be considered as a strike", True, BLACK)
                screen.blit(tuto_strike_text, (100, 100))
                pygame.display.flip()
                pygame.time.delay(3000)
                self.spawn_fruit('tuto',2)

            if self.missed_fruits > 2:
                tuto_strike_text2 = font.render("When you reach 3 strikes, it's Game Over", True, BLACK)
                screen.blit(tuto_strike_text2, (100, 100))
                pygame.display.flip()
                pygame.time.delay(3000)  # Delay for 3 seconds
                self.game_over = True
                return
                

    def tuto_combo(self):
        screen.blit(BACKGROUND_IMAGE, (0,0))
        self.tuto_freeze = False
        self.spawn_fruit('tuto',3)
        for fruit in self.fruits:
            fruit["letter"] = 'a'
        while not self.tuto_freeze:
            screen.blit(BACKGROUND_IMAGE, (0,0))
            self.update_fruits()
            self.draw_fruits()
            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if fruit["speed_y"] >0:
                self.tuto_freeze = True
                tuto_combo_text = font.render("Sometimes, fruits will have the same letter !", True, BLACK)
                screen.blit(tuto_combo_text, (100, 100))
                pygame.display.flip()
                time.sleep(3)
                tuto_run = True
                while tuto_run:
                    screen.blit(BACKGROUND_IMAGE, (0,0))
                    self.draw_fruits()
                    tuto_combo_text = font.render("If you slash them, you will do a combo !", True, BLACK)
                    screen.blit(tuto_combo_text, (100, 100))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.game_over = True
                        if event.type == pygame.KEYDOWN:
                            self.check_key_press(event.key)
                    pygame.display.flip()
                    if not self.fruits:
                        tuto_run = False
            screen.blit(BACKGROUND_IMAGE,(0,0))

    def tuto_ice(self):
        clock.tick(30)
        self.tuto_freeze = False
        screen.blit(BACKGROUND_IMAGE, (0,0))
        self.spawn_fruit('tuto_ice',1)
        self.spawn_fruit('tuto',2)
        while not self.tuto_freeze:
            screen.blit(BACKGROUND_IMAGE,(0,0))
            self.update_fruits()
            self.draw_fruits()
            pygame.display.flip()
            clock.tick(30)
            for fruit in self.fruits:
                if fruit["image"] == FRUIT_IMAGES["ice"]:
                    if fruit["speed_y"] > 0:
                        self.tuto_freeze = True
        while self.tuto_freeze:
            screen.blit(BACKGROUND_IMAGE, (0,0))
            tuto_ice_text = font.render("This is an icecube, if you slash it, you will stop time !", True, BLACK)
            screen.blit(tuto_ice_text, (100, 100))
            self.update_fruits()
            self.draw_fruits()
            pygame.display.flip()
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    self.check_key_press(event.key)
            if self.is_frozen and pygame.time.get_ticks() > self.freeze_end_time:
                self.is_frozen = False
                if ICE_SOUND:
                        ICE_SOUND.stop()
            clock.tick(30)
        while self.fruits:
            screen.blit(BACKGROUND_IMAGE, (0,0))
            self.update_fruits()
            self.draw_fruits()
            pygame.display.flip()
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    self.check_key_press(event.key)
            if self.is_frozen and pygame.time.get_ticks() > self.freeze_end_time:
                self.is_frozen = False
                if ICE_SOUND:
                        ICE_SOUND.stop()

    def tuto_bomb(self):
        self.tuto_freeze = False
        self.spawn_fruit('tuto_bomb',1)
        while not self.tuto_freeze:
            screen.blit(BACKGROUND_IMAGE, (0,0))
            self.update_fruits()
            self.draw_fruits()
            pygame.display.flip()
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            for fruit in self.fruits:
                if fruit["speed_y"] > 0:
                    self.tuto_freeze = True
                    tuto_bomb_text = font.render("THIS IS A BOMB, DO NOT SLASH IT", True, BLACK)
                    screen.blit(tuto_bomb_text, (100, 100))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    tuto_run = True
        while tuto_run:
            screen.blit(BACKGROUND_IMAGE,(0,0))
            tuto_bomb_text2 = font.render("IF YOU SLASH IT, IT'S GAME OVER", True, BLACK)
            screen.blit(tuto_bomb_text2, (100, 100))
            pygame.display.flip()
            pygame.time.delay(3000)
            self.tuto_freeze = False
            clock.tick(30)
            tuto_run = False

    # Function to run the game
    def run(self, difficulty, player):
        clock.tick(30)
        if difficulty == 'tuto':
            self.tuto_fruit()
            self.tuto_strike()
            self.tuto_combo()
            self.tuto_ice()
            self.tuto_bomb()
        else:
            while not self.game_over:
                # Background
                screen.blit(BACKGROUND_IMAGE, (0, 0))
                spawn_rate = self.difficulty_rates(difficulty)
                # Manage events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_over = True
                    if event.type == pygame.KEYDOWN:
                        self.check_key_press(event.key)

                # Generate new fruits
                if not self.is_frozen and random.random() < spawn_rate:
                    self.spawn_fruit(difficulty,count=1)

                # Update annd draw the fruits
                self.update_fruits()
                self.draw_fruits()

                # Display the score and the number of Strikes
                score_text = font.render(f"Score of {player} : {self.player_score}", True, BLACK)
                screen.blit(score_text, (10, 10))
                missed_text = font.render(f"Strike : {self.missed_fruits}", True, BLACK)
                screen.blit(missed_text, (10, 40))

                # After freeze, the game is no longer frozen
                if self.is_frozen and pygame.time.get_ticks() > self.freeze_end_time:
                    self.is_frozen = False
                    if ICE_SOUND:
                            ICE_SOUND.stop()

                # Check if the game is over
                if self.missed_fruits >= 3:
                    game_over_text = font.render("Game Over !", True, BLACK)
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    self.game_over = True

                pygame.display.flip()
                clock.tick(30)
            return self.player_score
    
    if ICE_SOUND:
        ICE_SOUND.stop()

if __name__ == "__main__":
    game = FruitSlicerGame()
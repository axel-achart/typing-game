# Importing Libraries
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

    # Function to get the fruit rates
    def get_fruit_rates(self,difficulty):
        if difficulty == 'easy':
            return 0.9
        if difficulty == 'medium':
            return 0.8
        if difficulty == 'hard':
            return 0.7
        return 0.9
    
    # Function to get the difficulty rates
    def difficulty_rates(self,difficulty):
        if difficulty == 'easy':
            return 0.05
        if difficulty == 'medium':
            return 0.04
        if difficulty == 'hard':
            return 0.03
        return 0.05

    # Function to spawn the fruit
    def spawn_fruit(self,difficulty, count=1):
        difficulty = self.difficulty
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
            if random.random() < special_spawn_rates:
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

    # Function to update the fruits
    def update_fruits(self):
        if self.is_frozen:
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
        for fruit in self.fruits:
            if key == ord(fruit["letter"].lower()):
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
    
    # Function to run the game
    def run(self, difficulty, player):
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
    game.run()
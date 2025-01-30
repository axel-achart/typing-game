import pygame
import random
import sys
import math

# -------------------------------------------- Configurations de la fenêtre --------------------------------------------#
pygame.init()

# Dimensions de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Slicer")
clock = pygame.time.Clock()

# Charger les images des fruits et bombes
FRUIT_IMAGES = {
    "apple": pygame.image.load(r"media\img\apple.png"),
    "banana": pygame.image.load(r"media\img\banana.png"),
    "pear": pygame.image.load(r"media\img\pear.png"),
    "watermelon": pygame.image.load(r"media\img\watermelon.png"),
    "bomb": pygame.image.load(r"media\img\bomb.png"),
    "ice": pygame.image.load(r"media\img\ice.png")
}

# Charger l'image de fond
BACKGROUND_IMAGE = pygame.image.load(r"media\img\background.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Charger l'image de l'explosion
EXPLOSION_IMAGE = pygame.image.load(r"media\img\explosion.png")
EXPLOSION_IMAGE = pygame.transform.scale(EXPLOSION_IMAGE, (80, 80))  # Redimensionner l'explosion

# Redimensionner les images à 80x80 dans le dict FRUIT_IMAGES
for key in FRUIT_IMAGES:
    FRUIT_IMAGES[key] = pygame.transform.scale(FRUIT_IMAGES[key], (80, 80))

# Police et texte
font = pygame.font.Font(None, 36)

# Charger les sons
pygame.mixer.init()
pygame.mixer.music.set_volume(2)
SLICE_SOUND = pygame.mixer.Sound(r"media\sounds\slice_sound.mp3")
BOMB_SOUND = pygame.mixer.Sound(r"media\sounds\bomb_sound.mp3")
ICE_SOUND = pygame.mixer.Sound(r"media\sounds\ice_sound.mp3")

class FruitSlicerGame:
    def __init__(self, difficulty, player):
        self.fruits = []  # Liste des fruits actifs à l'écran
        self.player_score = 0  # Score du joueur
        self.missed_fruits = 0  # Nombre de fruits manqués
        self.game_over = False  # État du jeu
        self.angle = 0  # Angle de rotation (non utilisé actuellement)
        self.is_frozen = False  # Indique si le jeu est gelé
        self.freeze_end_time = 0  # Temps où le gel doit se terminer
        self.difficulty = difficulty
        self.player = player

    def get_fruit_rates(self,difficulty):
        if difficulty == 'easy':
            return 0.9
        if difficulty == 'medium':
            return 0.8
        if difficulty == 'hard':
            return 0.7
        return 0.9
    def difficulty_rates(self,difficulty):
        if difficulty == 'easy':
            return 0.03
        if difficulty == 'medium':
            return 0.1
        if difficulty == 'hard':
            return 0.2
        return 0.03


    def spawn_fruit(self,difficulty, count=1):
        difficulty = self.difficulty
        fruit_spawn_rate = self.get_fruit_rates(difficulty)
        if not self.is_frozen and random.random() < fruit_spawn_rate:
            self.spawn_fruit(count=random.randint(1, 2))
        # Liste des fruits normaux
        NORMAL_FRUITS = ["apple", "banana", "pear", "watermelon"]
        # Liste des objets spéciaux (bombe et glacon)
        SPECIAL_OBJECTS = ["bomb", "ice"]
        
        for _ in range(count):
            # Position initiale du fruit
            spawn_x = random.randint(100, SCREEN_WIDTH - 100)
            spawn_y = SCREEN_HEIGHT - 150  # Les fruits apparaissent encore plus haut
            
            # Lettre associée au fruit
            assigned_letter = chr(random.randint(65, 90))
            
            # Choix du type de fruit avec probabilité réduite pour les objets spéciaux
            if random.random() < fruit_spawn_rate:  # 90% de chance d'avoir un fruit normal
                fruit_type = random.choice(NORMAL_FRUITS)
            else:
                fruit_type = random.choice(SPECIAL_OBJECTS)
            
            # Vitesse initiale
            horizontal_speed = random.uniform(-4, 4)  # Vitesse horizontale
            vertical_speed = random.uniform(-18, -12)  # Vitesse verticale
            gravity = 0.5  # Force de gravité
            
            # Ajout du fruit à la liste
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

    def update_fruits(self):
        if self.is_frozen:
            return # Ne pas mettre à jour les fruits si le jeu est gelé
        
        active_fruits = []
        for fruit in self.fruits:
            # Mise à jour de la position
            fruit["position_x"] += fruit["speed_x"]
            fruit["position_y"] += fruit["speed_y"]
            fruit["speed_y"] += fruit["gravity"]
            
            # Rotation du fruit
            fruit["rotation_angle"] += fruit["rotation_speed"]
            
            # Supprime les fruits qui sortent de l'écran par le bas
            if fruit["position_y"] > SCREEN_HEIGHT + 50:
                self.missed_fruits += 1
            else:
                active_fruits.append(fruit)

        self.fruits = active_fruits

    def check_key_press(self, key):
        remaining_fruits = []
        for fruit in self.fruits:
            if key == ord(fruit["letter"].lower()):
                if fruit["image"] == FRUIT_IMAGES["bomb"]:
                    BOMB_SOUND.play()
                    game_over_text = font.render("Game Over! You sliced a bomb", True, BLACK)
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    self.game_over = True
                elif fruit["image"] == FRUIT_IMAGES["ice"]:
                    self.player_score += 10
                    ICE_SOUND.play()
                    self.is_frozen = True
                    self.freeze_end_time = pygame.time.get_ticks() + 5000  # Gel pendant 5 secondes
                else:
                    self.player_score += 5
                    SLICE_SOUND.play()
                    # Ajouter une explosion à la position du fruit
                    self.explosions.append({
                        "position_x": fruit["position_x"],
                        "position_y": fruit["position_y"],
                        "start_time": pygame.time.get_ticks()
                    })
            else:
                remaining_fruits.append(fruit)
        self.fruits = remaining_fruits

    def draw_fruits(self):
        for fruit in self.fruits:
            # Rotation de l'image
            rotated_image = pygame.transform.rotate(fruit["image"], fruit["rotation_angle"])
            new_rect = rotated_image.get_rect(center=fruit["image"].get_rect(topleft=(fruit["position_x"], fruit["position_y"])).center)
            
            screen.blit(rotated_image, new_rect.topleft)
            text = font.render(fruit["letter"], True, BLACK)
            screen.blit(text, (fruit["position_x"] + 25, fruit["position_y"] + 25))  # Ajustement de la position du texte
        
        # Dessiner les explosions
        current_time = pygame.time.get_ticks()
        for explosion in self.explosions[:]:
            if current_time - explosion["start_time"] < 300:  # Afficher l'explosion pendant 300 ms
                screen.blit(EXPLOSION_IMAGE, (explosion["position_x"], explosion["position_y"]))
            else:
                self.explosions.remove(explosion)  # Supprimer l'explosion après 300 ms
        
    def run(self, difficulty, player):
        while not self.game_over:
            # Dessiner l'arrière-plan
            screen.blit(BACKGROUND_IMAGE, (0, 0))
            spawn_rate = self.difficulty_rates(difficulty)
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    self.check_key_press(event.key)

            if random.random() < spawn_rate:
                self.spawn_fruit(difficulty,count=random.randint(1, 2))

            # Mettre à jour et dessiner les fruits
            self.update_fruits()
            self.draw_fruits()

            # Afficher le score et les fruits manqués
            score_text = font.render(f"Score of {player}: {self.player_score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            missed_text = font.render(f"Strike: {self.missed_fruits}", True, BLACK)
            screen.blit(missed_text, (10, 40))

            # Reprise du jeu après le gel
            if self.is_frozen and pygame.time.get_ticks() > self.freeze_end_time:
                self.is_frozen = False

            # Vérifier si la partie est terminée
            if self.missed_fruits > 3:
                game_over_text = font.render("Game Over!", True, BLACK)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                self.game_over = True

            pygame.display.flip()
            clock.tick(30)
        return self.player_score

if __name__ == "__main__":
    game = FruitSlicerGame()
    game.run()
import pygame
import random
import sys
import math

# -------------------------------------------- Configurations de la fenêtre --------------------------------------------#
pygame.init()

# Dimensions de la fenêtre
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Slicer")
clock = pygame.time.Clock()

# Charger les images des fruits et bombes
FRUIT_IMAGES = {
    "apple": pygame.image.load(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\apple.png"),
    "banana": pygame.image.load(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\banana.png"),
    "pear": pygame.image.load(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\pear.png"),
    "watermelon": pygame.image.load(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\watermelon.png"),
    "bomb": pygame.image.load(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\bomb.png"),
    "ice": pygame.image.load(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\ice.png")
}

# Charger l'image de fond
BACKGROUND_IMAGE = pygame.image.load(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\background.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Redimensionner les images à 80x80 dans le dict FRUIT_IMAGES
for key in FRUIT_IMAGES:
    FRUIT_IMAGES[key] = pygame.transform.scale(FRUIT_IMAGES[key], (80, 80))

# Police et texte
font = pygame.font.Font(None, 36)

# Charger les sons
pygame.mixer.init()
BACKGROUND_MUSIC = pygame.mixer.Sound(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\background_music.mp3")
SLICE_SOUND = pygame.mixer.Sound(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\slice_sound.mp3")
BOMB_SOUND = pygame.mixer.Sound(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\bomb_sound.mp3")
ICE_SOUND = pygame.mixer.Sound(r"C:\\Users\\kylli\\Desktop\\Spe_ia\\typing-game\\Fruits\\ice_sound.mp3")

# Jouer la musique de fond en boucle
BACKGROUND_MUSIC.play(-1)


class FruitSlicerGame:
    def __init__(self):
        self.fruits = []  # Liste des fruits actifs à l'écran
        self.player_score = 0  # Score du joueur
        self.missed_fruits = 0  # Nombre de fruits manqués
        self.game_over = False  # État du jeu
        self.angle = 0  # Angle de rotation (non utilisé actuellement)

    def spawn_fruit(self, count=1):
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
            if random.random() < 0.9:  # 90% de chance d'avoir un fruit normal
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
        active_fruits = []
        for fruit in self.fruits:
            # Mise à jour de la position
            fruit["position_x"] += fruit["speed_x"]
            fruit["position_y"] += fruit["speed_y"]
            fruit["speed_y"] += fruit["gravity"]
            
            # Rotation du fruit
            fruit["rotation_angle"] += fruit["rotation_speed"]
            
            # Supprime les fruits qui sortent de l'écran par le bas
            if fruit["position_y"] > SCREEN_HEIGHT + 100:
                self.missed_fruits += 1
            else:
                active_fruits.append(fruit)

        self.fruits = active_fruits

    def check_key_press(self, key):
        remaining_fruits = []
        for fruit in self.fruits:
            if key == ord(fruit["letter"].lower()):
                if fruit["image"] == FRUIT_IMAGES["bomb"]:
                    self.game_over = True
                    BOMB_SOUND.play()
                elif fruit["image"] == FRUIT_IMAGES["ice"]:
                    self.player_score += 10
                    ICE_SOUND.play()
                else:
                    self.player_score += 5
                    SLICE_SOUND.play()
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


# Initialisation du jeu
game = FruitSlicerGame()

while not game.game_over:
    # Dessiner l'arrière-plan
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.game_over = True
        if event.type == pygame.KEYDOWN:
            game.check_key_press(event.key)

    # Ajouter des fruits périodiquement
    if random.random() < 0.03:
        game.spawn_fruit(count=random.randint(1, 2))

    # Mettre à jour et dessiner les fruits
    game.update_fruits()
    game.draw_fruits()

    # Afficher le score et les fruits manqués
    score_text = font.render(f"Score: {game.player_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    missed_text = font.render(f"Missed: {game.missed_fruits}", True, BLACK)
    screen.blit(missed_text, (10, 40))

    # Vérifier si la partie est terminée
    if game.missed_fruits > game.player_score:
        game_over_text = font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        game.game_over = True

    pygame.display.flip()
    clock.tick(30)

# Arrêter la musique de fond à la fin du jeu
BACKGROUND_MUSIC.stop()
pygame.quit()
import pygame
import random
import sys
#--------------------------------------------configurations de la fenetre--------------------------------------------#
# Initialisation de Pygame
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

# Police et texte
font = pygame.font.Font(None, 36)

# Variables de jeu
fruits = []
player_score = 0
missed_fruits = 0
game_over = False
clock = pygame.time.Clock()# Contrôle la vitesse de la boucle du jeu

# Charger une image pour les fruits
fruit_pictures = {
    "apple":pygame.image.load(r"C:\Users\kylli/Desktop\Spe_ia\typing-game\Fruits\apple.png"),
    "banana":pygame.image.load(r"C:\Users\kylli/Desktop\Spe_ia\typing-game\Fruits\banana.png"),
    "pear":pygame.image.load(r"C:\Users\kylli/Desktop\Spe_ia\typing-game\Fruits\pear.png"),
    "watermelon":pygame.image.load(r"C:\Users\kylli/Desktop\Spe_ia\typing-game\Fruits\watermelon.png")
}
# Redimensionner les images des fruits 50x50
for key in fruit_pictures:
    fruit_pictures[key] = pygame.transform.scale(fruit_pictures[key], (50, 50))

# Ajouter des fruits
def spawn_fruit(count=1):
    types_of_fruits = list(fruit_pictures.keys())
    for _ in range(count):
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        letter = chr(random.randint(65, 90))  # Lettre aléatoire (A-Z)
        fruit_type = random.choice(types_of_fruits)  # Choisir un fruit aléatoire
        fruits.append({
            "x": x, 
            "y": y, 
            "letter": letter,
            "image": fruit_pictures[fruit_type]  # Associer l'image correspondante
        })

# Dessiner les fruits
def draw_fruits():
    for fruit in fruits:
        screen.blit(fruit["image"], (fruit["x"], fruit["y"]))  # Dessiner l'image du fruit
        text = font.render(fruit["letter"], True, BLACK)  # Afficher la lettre
        screen.blit(text, (fruit["x"] + 15, fruit["y"] + 15))  # Positionner la lettre

# Vérifier si une touche correspond à un fruit
def check_key(key):
    global player_score, missed_fruits, fruits
    for fruit in fruits:
        if key == ord(fruit["letter"].lower()):  # Vérifie la touche
            fruits.remove(fruit)
            player_score += 1
            return
    missed_fruits += 1

# Boucle principale du jeu
while not game_over:
    screen.fill(WHITE)
    
    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            check_key(event.key)
    
    # Ajouter des fruits périodiquement
    if random.random() < 0.1:  # Probabilité d'apparition
        spawn_fruit(count=random.randint(2, 5))
    
    # Dessiner les fruits
    draw_fruits()
    
    # Afficher le player_score
    player_score_text = font.render(f"player_score: {player_score}", True, BLACK)
    screen.blit(player_score_text, (10, 10))
    
    # Afficher les fruits manqués
    missed_fruits_text = font.render(f"missed_fruits: {missed_fruits}", True, BLACK)
    screen.blit(missed_fruits_text, (10, 40))
    
    # Vérifier si la partie est terminée
    if missed_fruits >= 3:
        game_over_text = font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        game_over = True
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

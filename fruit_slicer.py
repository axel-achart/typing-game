import pygame, random, json, os
from gameplay import FruitSlicerGame
#----------------------Initialisations----------------------#
file_scores = 'scores.json' #file with each player and their scores
pygame.init()
pygame.mixer.init()
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# Variables de jeu
fruits = []
player_score = 0
missed_fruits = 0
# Initialisation Window
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fruit Slicer")
FONT = pygame.FONT.FONT(None, 40)
clock = pygame.time.Clock()
# Charger une image pour les fruits
fruit_images = {
    "apple":pygame.image.load(r"media\img\apple.png"),
    "banana":pygame.image.load(r"media\img\banana.png"),
    "pear":pygame.image.load(r"media\img\pear.png"),
    "watermelon":pygame.image.load(r"media\img\watermelon.png"),
    "bomb": pygame.image.load(r"media\img\bomb.png"),
    "ice": pygame.image.load(r"media\img\ice.png")
}
# Charger les sons
try:
    sound_menu = pygame.mixer.Sound(r"media\sounds\menu.mp3")
    sound_play = pygame.mixer.Sound(r"media\sounds\play.mp3")
    SLICE_SOUND = pygame.mixer.Sound(r"media\sounds\slice_sound.mp3")
    BOMB_SOUND = pygame.mixer.Sound(r"media\sounds\bomb_sound.mp3")
    ICE_SOUND = pygame.mixer.Sound(r"media\sounds\ice_sound.mp3")
except pygame.error as e:
    sound_menu = None
    sound_play = None
    SLICE_SOUND = None
    BOMB_SOUND = None
    ICE_SOUND = None
# Charger l'image de fond
BACKGROUND_IMAGE = pygame.image.load(r"media\img\background.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
# Redimensionner les images des fruits 50x50
for key in fruit_images:
    fruit_images[key] = pygame.transform.scale(fruit_images[key], (75, 75))



#----------------------Fonctions----------------------#
def text_display(text, x, y, color):
    text_render=FONT.render(text,True,color)
    screen.blit(text_render,(x,y))

def menu_player(ready,current_player):
    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        text_display("Welcome, Please choose your Player Name",50,50,BLACK)
        text_display("Press 1 to choose from a known Player Name",50,100,BLACK)
        text_display("Press 2 to create a Player Name",50,150,BLACK)
        text_display("Press ESCAPE if you want to keep your username",25,HEIGHT-50,BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player=menu_player_known()
                    if player:
                        return player
                elif event.key == pygame.K_2:
                    player=menu_player_new()
                    if player:
                        return player                
                if ready == 1:
                    if event.key == pygame.K_ESCAPE:
                        return current_player
        clock.tick(30)

def menu_player_known():
    screen.fill(WHITE)
    clock = pygame.time.Clock()
    players = list(scores_load().keys())
    players_per_page = 10
    current_page = 0
    total_pages = (len(players)+players_per_page - 1) // players_per_page
    if players:
        while True:
            index_start = current_page * players_per_page
            index_end = index_start + players_per_page
            screen.fill(WHITE)
            for i, player in enumerate(players[index_start:index_end]):
                text_display(f"Player {i}:{player}",50, 100 +50*i,BLACK)
            text_display("Welcome, Please choose your Player Name",50,50,BLACK)
            text_display(f"Page{current_page+1}/{total_pages}",50,HEIGHT-200,BLACK)
            text_display("Press N to go to next page",50,HEIGHT-150,BLACK)
            text_display("Press P to go to previous page",50,HEIGHT-100,BLACK)
            text_display("Press ESCAPE if you want to keep your username",50,HEIGHT-50,BLACK)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        index = (event.key - pygame.K_1)+index_start
                        if index < len(players):
                            return players[index]
                    if event.key == pygame.K_0 and len(players) >= 10:
                        return players[9+index_start]
                    if event.key == pygame.K_p:
                        if current_page > 0:
                            current_page-=1
                    if event.key == pygame.K_n:
                        if index_end<len(players):
                            current_page+=1                   
            clock.tick(30)
    else:
        text_display("No player found",250,250,BLACK)
        pygame.display.flip()
        pygame.time.wait(1500)
        return
    
def menu_player_new():
    screen.fill(WHITE)
    clock = pygame.time.Clock()
    player = ''
    while True:
        screen.fill(WHITE)
        text_display("Add a new player",50,50,BLACK)
        text_display("Type your username",50,100,BLACK)
        text_display(f"{player}",50,150,BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player:
                        menu_player_add(player)
                        return player
                elif event.key == pygame.K_BACKSPACE:
                    player = player[:-1]
                else:
                    letter=event.unicode
                    if letter.isalpha():
                        player +=letter 
                if event.key == pygame.K_ESCAPE:
                    return
        clock.tick(30)
        
def menu_player_add(player):
    screen.fill(WHITE)
    scores = scores_load()
    if player not in scores:
        scores[player]={"easy":[], "medium":[], "hard":[]}
    with open(file_scores, "w") as f:
        json.dump(scores, f, indent=4)

def menu_difficulty(ready,current_difficulty):
    screen.fill(WHITE)
    clock = pygame.time.Clock()
    while True:
        text_display("Please choose the difficulty",50,50,BLACK)
        text_display("Press 1 for Easy mode",50,HEIGHT-200,BLACK)
        text_display("Press 2 for Medium mode",50,HEIGHT-150,BLACK)
        text_display("Press 3 for Hard mode",50,HEIGHT-100,BLACK)
        text_display("Press ESCAPE if you want to keep your set difficulty",50,HEIGHT-50,BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'easy'
                elif event.key == pygame.K_2:
                    return 'medium'
                elif event.key == pygame.K_3:
                    return 'hard'
                if ready == 1:
                    if event.key == pygame.K_ESCAPE:
                        return current_difficulty
        clock.tick(30)

def menu_gamemode(ready,current_gamemode):
    screen.fill(WHITE)
    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        text_display("Please choose the gamemode",50,50,BLACK)
        text_display("Press 1 for mode.1",50,HEIGHT-200,BLACK)
        text_display("Press 2 for mode.2",50,HEIGHT-150,BLACK)
        text_display("Press 3 for mode.3",50,HEIGHT-100,BLACK)
        text_display("Press ESCAPE if you want to keep your set gamemode",50,HEIGHT-50,BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'mode.1'
                elif event.key == pygame.K_2:
                    return 'mode.2'
                elif event.key == pygame.K_3:
                    return 'mode.3'
                if ready == 1:
                    if event.key == pygame.K_ESCAPE:
                        return current_gamemode
        clock.tick(30)

def menu_scores():
    screen.fill(WHITE)
    clock = pygame.time.Clock()
    scores = scores_load()
    players_per_page = 1
    current_page = 0
    total_pages = (len(scores)+players_per_page - 1) // players_per_page
    while True:
        screen.fill(WHITE)
        text_display("Scoreboard",50,50, BLACK)
        index_start = current_page * players_per_page
        index_end = index_start + players_per_page
        players_list = list(scores.items())[index_start:index_end]
        y_offset = 100
        for player, scores_difficulty in players_list:
            text_display(f"Player : {player}",50,y_offset,BLACK)
            y_offset+=50
            for difficulte, player_scores in scores_difficulty.items():
                text_display(f"Difficulty : {difficulte}",70,y_offset,BLACK)
                y_offset+=80
                if player_scores:
                    text_display(f"Highest Score : {max(player_scores)} points", 90,y_offset-40,BLACK)
                else:
                    text_display("No Score",90,y_offset-40,BLACK)
        text_display(f"Page{current_page+1}/{total_pages}",50,HEIGHT-150,BLACK)
        text_display("Press N to go to next page",50,HEIGHT-125,BLACK)
        text_display("Press P to go to previous page",50,HEIGHT-100,BLACK)
        text_display("Press R to reset scoreboard",50,HEIGHT-75,BLACK)
        text_display("Press ESCAPE if you want to keep your username",50,HEIGHT-50,BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if current_page > 0:
                        current_page-=1
                if event.key == pygame.K_n:
                    if index_end<len(scores):
                        current_page+=1          
                elif event.key == pygame.K_3:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_r:
                    scores_reset()
                    return      # return to menu after reset
        clock.tick(30)
        
def scores_load():
    if not os.path.exists(file_scores):
        return {}
    try:
        with open(file_scores, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    
def scores_save(player, score, difficulty):
    screen.fill(WHITE)
    scores = scores_load()
    if player not in scores:
        scores[player] = {"easy":[], "medium":[], "hard":[]}
    if not scores[player][difficulty] or score > max(scores[player][difficulty]):
        scores[player][difficulty]=[score]
    with open(file_scores,"w") as f:
        json.dump(scores,f,indent=4)

# Reset the scores
def scores_reset():
    with open(file_scores,"w") as f:
        f.write("{}")
    
def menu_main():
    player = menu_player(0,0)
    gamemode = menu_gamemode(0,0)
    difficulty = menu_difficulty(0,0)
    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        text_display("Fruit Slicer",50,50,BLACK)
        text_display("Press 1 to play",50,100,BLACK)
        text_display("Press 2 to see the scores",50,150,BLACK)
        text_display("Press 3 to change the difficulty",50,200,BLACK)
        text_display("Press 4 to change the player",50,250,BLACK)
        text_display("Press 5 to change the gamemode",50,300,BLACK)
        text_display("Press 6 to quit",50,350,BLACK)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play(player, difficulty, gamemode, missed_fruits, player_score)
                if event.key == pygame.K_2:
                    menu_scores()
                if event.key == pygame.K_3:
                    difficulty = menu_difficulty(1,difficulty)
                if event.key == pygame.K_4:
                    player = menu_player(1,player)
                if event.key == pygame.K_5:
                    gamemode = menu_gamemode(1,gamemode)
                if event.key == pygame.K_6:
                    pygame.quit()
                    return
        clock.tick(30)

# Générer des fruits
def generate_item(count = 1):
    types_of_fruits = list(fruit_images.keys())
    for _ in range(count):
        x = random.randint(0, WIDTH - 50)    # Coordonnée x aléatoire
        y = random.randint(50, HEIGHT - 50)  # Coordonnée y aléatoire
        letter = chr(random.randint(65, 90))  # Lettre aléatoire (A-Z)
        fruit_type = random.choice(types_of_fruits)  # Choisir un fruit aléatoire

        fruits.append({
            "x": x, 
            "y": y, 
            "letter": letter,
            "image": fruit_images[fruit_type]  # Associer l'image correspondante
        })

# Dessiner les fruits
def item_display():
    for fruit in fruits:
        screen.blit(fruit["image"], (fruit["x"], fruit["y"]))  # Dessiner l'image du fruit
        text = FONT.render(fruit["letter"], True, BLACK)  # Afficher la lettre
        screen.blit(text, (fruit["x"] + 15, fruit["y"] + 15))  # Positionner la lettre

# Vérifier si une touche correspond à un fruit
def item_check(key, player_score, missed_fruits):
    for item in fruits:
        if key == ord(item["letter"].lower()):  # Vérifie la touche
            fruits.remove(item)
            player_score += 1
            return 
        else:
            missed_fruits += 1


#----------------------Class Jeu----------------------#
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
            spawn_x = random.randint(100, WIDTH - 100)
            spawn_y = HEIGHT - 150  # Les fruits apparaissent encore plus haut
            
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
                "image": fruit_images[fruit_type],
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
            if fruit["position_y"] > HEIGHT + 100:
                self.missed_fruits += 1
            else:
                active_fruits.append(fruit)

        self.fruits = active_fruits

    def check_key_press(self, key):
        remaining_fruits = []
        for fruit in self.fruits:
            if key == ord(fruit["letter"].lower()):
                if fruit["image"] == fruit_images["bomb"]:
                    self.game_over = True
                    BOMB_SOUND.play()
                elif fruit["image"] == fruit_images["ice"]:
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
            text = FONT.render(fruit["letter"], True, BLACK)
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
    score_text = FONT.render(f"Score: {game.player_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    missed_text = FONT.render(f"Missed: {game.missed_fruits}", True, BLACK)
    screen.blit(missed_text, (10, 40))

    # Vérifier si la partie est terminée
    if game.missed_fruits > game.player_score:
        game_over_text = FONT.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        game.game_over = True

    pygame.display.flip()
    clock.tick(30)


pygame.quit()

# Boucle principale du jeu
def play(difficulty, gamemode):
    if sound_menu:
        sound_menu.stop()
        if sound_play:
            sound_play.play(-1)
    while True:
        game = FruitSlicerGame(difficulty, gamemode)
    
    
    
    

if __name__ == "__main__":
    if sound_menu:
        sound_menu.play(-1)
    menu_main()
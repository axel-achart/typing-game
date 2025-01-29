# A rajouter :
# fonction pour reset le score
# potentiellement utilisé des class
# ajouter son/bruitage


import pygame, random, json, os

file_scores = 'scores.json' #file with each player and their scores

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FONT = pygame.font.Font(None, 40)

# Variables de jeu
fruits = []
player_score = 0
missed_fruits = 0
clock = pygame.time.Clock()   # Contrôle la vitesse de la boucle du jeu

# Charger une image pour les fruits
fruit_pictures = {
    "apple":pygame.image.load(r"typing-game\Fruits\apple.png"),
    "banana":pygame.image.load(r"typing-game\Fruits\banana.png"),
    "pear":pygame.image.load(r"typing-game\Fruits\pear.png"),
    "watermelon":pygame.image.load(r"typing-game\Fruits\watermelon.png"),
    "bomb":pygame.image.load(r"typing-game\Fruits\bomb.png"),
    "ice":pygame.image.load(r"typing-game\Fruits\ice.png")
}

# Charger les sons
try:
    sound_menu = pygame.mixer.Sound(r"typing-game\sounds\menu.mp3")
    sound_play = pygame.mixer.Sound(r"typing-game\sounds\play.mp3")
except pygame.error as e:
    sound_menu = None
    sound_play = None

# Redimensionner les images des fruits 50x50
for key in fruit_pictures:
    fruit_pictures[key] = pygame.transform.scale(fruit_pictures[key], (50, 50))

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fruit Slicer")



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
    types_of_fruits = list(fruit_pictures.keys())
    for _ in range(count):
        x = random.randint(0, WIDTH - 50)    # Coordonnée x aléatoire
        y = random.randint(50, HEIGHT - 50)  # Coordonnée y aléatoire
        letter = chr(random.randint(65, 90))  # Lettre aléatoire (A-Z)
        fruit_type = random.choice(types_of_fruits)  # Choisir un fruit aléatoire

        fruits.append({
            "x": x, 
            "y": y, 
            "letter": letter,
            "image": fruit_pictures[fruit_type]  # Associer l'image correspondante
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

# Boucle principale du jeu
def play(player, difficulty, gamemode, missed_fruits, player_score):
    if sound_menu:
        sound_menu.stop()
        if sound_play:
            sound_play.play(-1)
    game_over = False
    while not game_over:
        screen.fill(WHITE)

        
        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                item_check(event.key)
        
        # Ajouter des fruits périodiquement
        if random.random() < 0.03:  # Probabilité d'apparition
            generate_item(count=random.randint(1, 3))
        
        # Dessiner les fruits
        item_display()
        
        # Afficher le player
        player_text = FONT.render(f"player : {player}", True, BLACK)
        screen.blit(player_text, (10, 10))

        # Afficher la difficulté
        difficulty_text = FONT.render(f"difficulté : {difficulty}", True, BLACK)
        screen.blit(difficulty_text, (10, 40))

        # Afficher le player_score
        player_score_text = FONT.render(f"player_score: {player_score}", True, BLACK)
        screen.blit(player_score_text, (10, 70))
        
        # Afficher les strikes
        missed_fruits_text = FONT.render(f"missed_fruits: {missed_fruits}", True, BLACK)
        screen.blit(missed_fruits_text, (10, 100))
        
        # Vérifier si la partie est perdue
        if missed_fruits >= 3:
            game_over_text = FONT.render("Game Over!", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            game_over = True
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    if sound_menu:
        sound_menu.play(-1)
    menu_main()
# Importing Libraries
import pygame, random, json, os
from gameplay import FruitSlicerGame

# Join file scores.json
file_scores = 'scores.json'

# Initialisation PyGame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Window Dimension
WIDTH = 800
HEIGHT =  600

# Font and text
FONT = pygame.font.Font(None, 40)

# Variables
fruits = []
player_score = 0
missed_fruits = 0

# Initialisation Window
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fruit Slicer")

# Fruits loading
fruit_images = {
    "apple":pygame.image.load(r"media\img\apple.png"),
    "banana":pygame.image.load(r"media\img\banana.png"),
    "pear":pygame.image.load(r"media\img\pear.png"),
    "watermelon":pygame.image.load(r"media\img\watermelon.png"),
}

# Sounds loading
try:
    sound_menu = pygame.mixer.Sound(r"media\sounds\menu.mp3")
    sound_play = pygame.mixer.Sound(r"media\sounds\play.mp3")
except pygame.error as e:
    sound_menu = None
    sound_play = None

# Resize images fruits
for key in fruit_images:
    fruit_images[key] = pygame.transform.scale(fruit_images[key], (70, 70))

# Function to display text
def text_display(text, x, y, color):
    text_render=FONT.render(text,True,color)
    screen.blit(text_render,(x,y))

# Function to ask player
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

# Function to choose a player from the list
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

# Function to create a new player
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

# Function to add a player in scores.json
def menu_player_add(player):
    screen.fill(WHITE)
    scores = scores_load()
    if player not in scores:
        scores[player]={"easy":[], "medium":[], "hard":[]}
    with open(file_scores, "w") as f:
        json.dump(scores, f, indent=4)

# Function to choose the difficulty
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

# Function to choose the gamemode
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

# Function to display the scoreboard
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
                    return
        clock.tick(30)

# Load the scores from the file
def scores_load():
    if not os.path.exists(file_scores):
        return {}
    try:
        with open(file_scores, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

# Reset the scores
def scores_reset():
    with open(file_scores,"w") as f:
        f.write("{}")
    
# Main menu
def menu_main():
    player = menu_player(0,0)
    difficulty = menu_difficulty(0,0)
    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        text_display("Fruit Slicer",50,50,BLACK)
        text_display("Press 1 to play",50,100,BLACK)
        text_display("Press 2 to see the scores",50,150,BLACK)
        text_display("Press 3 to change the difficulty",50,200,BLACK)
        text_display("Press 4 to change the player",50,250,BLACK)
        text_display("Press 5 to go to the tutorial",50,350,BLACK)
        text_display("Press 6 to quit",50,400,BLACK)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play(player, difficulty)
                if event.key == pygame.K_2:
                    menu_scores()
                if event.key == pygame.K_3:
                    difficulty = menu_difficulty(1,difficulty)
                if event.key == pygame.K_4:
                    player = menu_player(1,player)
                if event.key == pygame.K_5:
                    play('tuto','tuto')
                if event.key == pygame.K_6:
                    pygame.quit()
                    return
        clock.tick(30)

# Function to save score from the game
def save_scores(player, difficulty, player_score):
    scores = scores_load()

    # Check if the player is in the scoreboard and it's not the tuto
    if player not in scores and player!='tuto':
        scores[player] = {"easy": 0, "medium": 0, "hard": 0}

    # Integrate the score if it is higher than the previous one
    if player in scores:
        if player_score > max(scores[player][difficulty], default=0):
            scores[player][difficulty] = [player_score]
    with open(file_scores,"w") as f:
        json.dump(scores,f,indent=4)

# Function to play the game
def play(player, difficulty):
    if sound_menu:
        sound_menu.stop()
        if sound_play:
            sound_play.play(-1)

    game = FruitSlicerGame(difficulty,player)
    if difficulty == 'tuto':
        game.run(difficulty,player)
    else:
        final_score = game.run(difficulty,player)

    # Save the score
        save_scores(player, difficulty, final_score)

    if sound_play:
        sound_play.stop()
        if sound_menu:
            sound_menu.play(-1)
    screen.fill(WHITE)
    return
    

if __name__ == "__main__":
    if sound_menu:
        sound_menu.play(-1)
    menu_main()
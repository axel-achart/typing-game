import pygame
import json
import os

file_scores = 'scores.json'#file with each player and their scores


def menu_player(ready,current_player):
    clock = pygame.time.Clock()
    while True:
        #display player choices
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return menu_player_known()
                elif event.key == pygame.K_2:
                    return menu_player_new()
                if ready == 1:
                    if event.key == pygame.K_ESCAPE:
                        return current_player
        clock.tick(30)

def menu_player_known():
    clock = pygame.time.Clock()
    players = list(scores_load().keys())  # Get the list of player names
    if players:
        while True:            
            #pagination
            #display the players for the user to choose from
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        index = event.key - pygame.K_1
                        if index < len(players):
                            return players[index]
                    if event.key == pygame.K_0 and len(players) >= 10:
                        return players[9]
            clock.tick(30)
    
def menu_player_new():
    clock = pygame.time.Clock()
    player = ''
    while True:
        #display the player name as he types it
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
        clock.tick(30)
        
def menu_player_add(player):
    scores = scores_load()
    if player not in scores:
        scores[player]={"easy":[], "medium":[], "hard":[]}  # Ajoute un nouveau joueur avec des scores vides
    with open(file_scores, "w") as f:
        json.dump(scores, f, indent=4)

def menu_difficulty(ready,current_difficulty):
    clock = pygame.time.Clock()
    while True:
        #display difficulty choices
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

def menu_scores():
    clock = pygame.time.Clock()
    while True:
        #pagination
        #for loop, to display each scores, for each difficulties, for each player
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    index = +1
                    #next page
                elif event.key == pygame.K_2:
                    index = -1
                    #previous page
                elif event.key == pygame.K_3:
                    return                
                if event.key == pygame.K_ESCAPE:
                    return
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
    scores = scores_load()
    if player not in scores:
        scores[player] = {"easy":[], "medium":[], "hard":[]}
    if not scores[player][difficulty] or score > max(scores[player][difficulty]):
        scores[player][difficulty]=[score]
    with open(file_scores,"w") as f:
        json.dump(scores,f,indent=4)
    
def menu_main():
    player = menu_player(0,0)
    difficulty = menu_difficulty(0,0)
    clock = pygame.time.Clock()
    while True:
        #display the menus choices
        #Play
        #Scores
        #Difficulty
        #Player
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play(player,difficulty)
                if event.key == pygame.K_2:
                    menu_scores()
                if event.key == pygame.K_3:
                    difficulty = menu_difficulty(1,difficulty)
                if event.key == pygame.K_4:
                    player = menu_player(1,player)
                if event.key == pygame.K_5:
                    pygame.quit()
                    return
        clock.tick(30)
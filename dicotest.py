import pygame

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 800  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 40)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fruit Sclicer")

def coords_generate():


def item_display():
    


def text_display(text, x, y, color):
    text_render=FONT.render(text,True,color)
    screen.blit(text_render,(x,y))

class item:
    def __init__(self,image,xy,letter):
        self.xy = 
        self.image = images_load(self)
        self.letter = letter_associate(self)

    def item_display(self):

        text_display(self.image,self.x,)

class fruit(item):

class special(item):


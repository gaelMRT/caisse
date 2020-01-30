#demande l'installation locale de pygame pour python3
import sys,time,pygame
from store import Store


pygame.init()
pygame.display.set_caption('Migros Simulator 2k20')

store = Store(800,600,10,50)

size = width, height = 800,600

black = 0,0,0

white = 255,255,255
red = 255,0,0
green = 0,255,0


window = pygame.display.set_mode(store._size)


font = pygame.font.Font('freesansbold.ttf',32)

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    store.makingMove()
    window.fill(white)

    store.draw(window,font)

    time.sleep(0.01)
    pygame.display.flip()

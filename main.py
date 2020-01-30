import sys,time,pygame
from store import Store
from pygame import gfxdraw


pygame.init()

store = Store()

size = width, height = 800,600
speed = [2,2]

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

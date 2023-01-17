import pygame
import sys
from board import Board

def play(screen, clock):
    #Constants
    BACKGROUND_COLOUR = (100, 100, 100)

    pygame.display.set_caption("Play")

    # Initialise background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BACKGROUND_COLOUR)

    BoardInput = Board((0, 0)).get_BoardInput()
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    BoardInput.click_down()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    BoardInput.click_up()
                    


                    
        
        BoardInput.draw(background)
        screen.blit(background, (0, 0))
        pygame.display.flip()
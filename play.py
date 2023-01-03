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

    board = Board((0, 0))
    selected_coords = None
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.set_is_dragging(True)
                    selected_coords = board.get_mouse_square()
                    board.set_selected_piece_coords(selected_coords)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    board.set_is_dragging(False)
                    new_selected_coords = board.get_mouse_square()
                    if new_selected_coords == None:
                        continue
                    if new_selected_coords != selected_coords:
                        board.move(selected_coords, new_selected_coords)
                        board.set_selected_piece_coords(None)


                    
        
        board.draw(background)
        screen.blit(background, (0, 0))
        pygame.display.flip()
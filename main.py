import pygame
import sys
from components import Button
from play import play


def main():
    # Constants
    WIDTH, HEIGHT = 800, 500
    BACKGROUND_COLOUR = (40, 40, 40)
    BUTTON_COLOUR = (130, 130, 130)
    BUTTON_HIGHLIGHT_COLOUR = (200, 200, 200)
    BUTTON_DIMENSIONS = (WIDTH // 5, HEIGHT // 6)
    PLAY_BUTTON_POS = (WIDTH // 2 + 5, (HEIGHT - BUTTON_DIMENSIONS[1]) // 2)
    ANALYSIS_BUTTON_POS = (WIDTH // 2 - 5 - BUTTON_DIMENSIONS[0], (HEIGHT - BUTTON_DIMENSIONS[1]) // 2)
    
    # Initialise pygame
    pygame.init()
    pygame.display.set_caption("Chess")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    # Initialise background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BACKGROUND_COLOUR)
    
    #Initialise buttons
    buttons = []
    buttons.append(Button(
                        PLAY_BUTTON_POS,
                        BUTTON_DIMENSIONS[0],
                        BUTTON_DIMENSIONS[1],
                        BUTTON_COLOUR,
                        BUTTON_HIGHLIGHT_COLOUR,
                        text='Play',
                        on_click=play,
                        on_click_args=(screen, clock)
                        )
                   )
    
    buttons.append(Button(
                        ANALYSIS_BUTTON_POS,
                        BUTTON_DIMENSIONS[0],
                        BUTTON_DIMENSIONS[1],
                        BUTTON_COLOUR,
                        BUTTON_HIGHLIGHT_COLOUR,
                        text='Analysis',
                        on_click=None
                        )
                   )
    
    # Event loop
    while True:
        clock.tick(30)
        mouse_pos = pygame.mouse.get_pos()
        for b in buttons:
            b.is_hovered = b.shape.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for b in buttons:
                        if b.is_hovered:
                            b.click()
        
        for b in buttons:
            b.draw(background)

        screen.blit(background, (0, 0))
        pygame.display.flip()
    

if __name__ == '__main__':
    main()
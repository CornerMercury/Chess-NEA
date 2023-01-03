import pygame


class Button:
    def __init__(self, pos, width, height, colour, highlight_colour=None,
                 text=None, text_colour=(0, 0, 0), on_click=None, on_click_args=None):
        self.pos = pos
        self.width = width
        self.height = height
        self.colour = colour
        self.highlight_colour = highlight_colour
        if highlight_colour == None:
            self.highlight_colour = colour
            
        self.text = text
        if text != None:
            self.has_text = True
            self.font = pygame.font.SysFont('Arial', 50)
            self.text_img = self.font.render(self.text, True, text_colour)
            self.text_width = self.text_img.get_width()
            self.text_height = self.text_img.get_height()
            
        self.on_click = on_click
        self.on_click_args = on_click_args
        self.shape = pygame.Rect(pos, (width, height))
        self.is_hovered = False
        
    def draw(self, surface):
        if self.is_hovered:
            pygame.draw.rect(surface, self.highlight_colour, self.shape)
        else:
            pygame.draw.rect(surface, self.colour, self.shape)
        
        if self.has_text:
            surface.blit(self.text_img,
                            (
                            self.pos[0] + self.width // 2 - self.text_width // 2,
                            self.pos[1] + self.height // 2 - self.text_height // 2
                            )
                        )
        
    def click(self):
        return self.on_click(*self.on_click_args)
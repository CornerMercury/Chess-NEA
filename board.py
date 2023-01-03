# Chess Board Class
import pygame
from piece import King, Queen, Rook, Knight, Bishop, Pawn, Piece

class Board:
    DEFAULT_BOARD_STATE = [
                            [
                                Rook('d'), Knight('d'), Bishop('d'), Queen('d'),
                                King('d'), Bishop('d'), Knight('d'), Rook('d')
                            ],
                            [Pawn('d') for _ in range(8)],
                            [None for _ in range(8)],
                            [None for _ in range(8)],
                            [None for _ in range(8)],
                            [None for _ in range(8)],
                            [Pawn('l') for _ in range(8)],
                            [
                                Rook('l'), Knight('l'), Bishop('l'), Queen('l'),
                                King('l'), Bishop('l'), Knight('l'), Rook('l')
                            ]
                        ]
    
    select_colour = (255, 0, 0)
    
    def __init__(self, pos, square_width=60, board_state=DEFAULT_BOARD_STATE,
                 light_colour=(238, 238, 210), dark_colour=(118, 150, 86)):
        self.__board_state = board_state
        # Update pieces with correct positions
        for i, row in enumerate(self.__board_state):
            for j, piece in enumerate(row):
                if piece:
                    piece.set_pos((i, j))

        self.__pos = pos
        self.__square_width = square_width
        self.__light_colour = light_colour
        self.__dark_colour = dark_colour
        self.__surface = pygame.Surface((self.__square_width * 8, self.__square_width * 8))
        self.__selected_piece_coords = None
        self.__is_dragging = False

    def set_selected_piece_coords(self, coords):
        if (coords == None or
            coords == self.__selected_piece_coords or
            self.__board_state[coords[0]][coords[1]] == None):
            self.__selected_piece_coords = None
            return

        self.__selected_piece_coords = coords

    def set_is_dragging(self, is_dragging):
        self.__is_dragging = is_dragging

    def get_mouse_square(self):
        mouse_pos = pygame.mouse.get_pos()
        x, y = (
            (mouse_pos[0] - self.__pos[0]) // self.__square_width,
            (mouse_pos[1] - self.__pos[1]) // self.__square_width
        )
        if 0 <= x <= 7 and 0 <= y <= 7:
            return (y, x)
        
        return None


    def move(self, start_pos, end_pos):
        pass

    def get_all_valid_moves(self):
        moves = []
        for i, row in enumerate(self.__board_state):
            for j, piece in enumerate(row):
                moves += piece.get_pseudo_valid_moves(self.__board_state)

    
    def draw(self, surface, select_colour=select_colour):
        for i, row in enumerate(self.__board_state):
            for j, piece in enumerate(row):
                square_coords = (j * self.__square_width, i * self.__square_width)
                # Draw checkered squares
                if (i + j) % 2 == 0:
                    pygame.draw.rect(
                        self.__surface,
                        self.__light_colour,
                        pygame.Rect(
                            square_coords,
                            (self.__square_width, self.__square_width)
                        )
                    )
                else:
                    pygame.draw.rect(
                        self.__surface,
                        self.__dark_colour,
                        pygame.Rect(
                            square_coords,
                            (self.__square_width, self.__square_width)
                        )
                    )

                # Draw pieces
                if isinstance(piece, Piece):
                    if not(self.__is_dragging and self.__selected_piece_coords == (i , j)):
                        self.__surface.blit(
                            pygame.transform.scale(
                                piece.image,
                                (self.__square_width, self.__square_width)
                            ),
                            square_coords
                        )
        
        # Draw highlighted square
        if self.__selected_piece_coords:
            highlight_rect = pygame.Rect(
                (
                    self.__selected_piece_coords[1] * self.__square_width,
                    self.__selected_piece_coords[0] * self.__square_width
                ),
                (
                    self.__square_width,
                    self.__square_width
                )
            )
            pygame.draw.rect(self.__surface, select_colour, highlight_rect, 2)

        
        if self.__is_dragging and self.__selected_piece_coords:
            y, x = self.__selected_piece_coords
            piece =  self.__board_state[y][x]
            mouse_pos = pygame.mouse.get_pos()
            self.__surface.blit(
                            pygame.transform.scale(
                                piece.image,
                                (self.__square_width, self.__square_width)
                            ),
                            (
                                mouse_pos[0] - self.__pos[0] - self.__square_width // 2,
                                mouse_pos[1] - self.__pos[1] - self.__square_width // 2
                            )
                        )

                        
        surface.blit(self.__surface, self.__pos)
        
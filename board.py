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
        # Update pieces with correct positions and board
        for i, row in enumerate(self.__board_state):
            for j, piece in enumerate(row):
                if piece:
                    piece.set_pos((i, j))
        
        self.__BoardInput = BoardInput(self)
        self.__played_moves = []
        self.__pos = pos
        self.__square_width = square_width
        self.__light_colour = light_colour
        self.__dark_colour = dark_colour
        self.__surface = pygame.Surface((self.__square_width * 8, self.__square_width * 8))
        self.__white_turn = True
        self.__valid_moves = None
        self.get_all_valid_moves()

    def get_BoardInput(self):
        return self.__BoardInput

    def get_mouse_square(self):
        mouse_pos = pygame.mouse.get_pos()
        converted_pos = (
            (mouse_pos[1] - self.__pos[1]) // self.__square_width,
            (mouse_pos[0] - self.__pos[0]) // self.__square_width
        )
        if self.pos_in_bounds(converted_pos):
            return converted_pos
        
        return None
    
    def pos_in_bounds(self, pos):
        return (0 <= pos[0] < len(self.__board_state[0]) and
                0 <= pos[1] < len(self.__board_state))
    
    def get_piece(self, pos):
        return self.__board_state[pos[0]][pos[1]]
    
    def get_piece_is_white(self, pos):
        piece = self.__board_state[pos[0]][pos[1]]
        if piece:
            return piece.get_is_white()
        return None

    def move(self, move, extra_replace=None):
        start_pos, end_pos = move
        if start_pos != end_pos and start_pos != None and end_pos != None and (start_pos, end_pos) in self.__valid_moves:
            end_y, end_x = end_pos
            start_y, start_x = start_pos
            self.__board_state[end_y][end_x] = self.__board_state[start_y][start_x]
            self.__board_state[start_y][start_x] = None
            self.__board_state[end_y][end_x].set_pos((end_y, end_x))
            if extra_replace:
                replace_y, replace_x = extra_replace[0]
                self.__board_state[replace_y][replace_x] = extra_replace[1]
                
            self.__white_turn = not(self.__white_turn)
            self.__played_moves.append((start_pos, end_pos, extra_replace))
            self.get_all_valid_moves()
            return True
        
        return False

    def get_all_valid_moves(self):
        moves = []
        for i, row in enumerate(self.__board_state):
            for j, piece in enumerate(row):
                if piece and piece.get_is_white() == self.__white_turn:
                    for move in piece.get_pseudo_moves():
                        if self.is_valid_move(move):
                            moves.append(((i, j), move[0]))
        
        self.__valid_moves = moves
        
    
    def is_valid_move(self, move):
        # move is (final_pos, final_pos_colour,
        # #extra_condition
        # (bool, condition_pos, condition_pos_colour))
        # extra condition could be en passant or castle
        # True is en passant and False is castle
        if (self.pos_in_bounds(move[0]) and
            self.get_piece_is_white(move[0]) == move[1]):
            if len(move) != 3:
                return True
            
            extra_condition, condition_pos, condition_pos_colour = move[2]
            
            if extra_condition:
                if (self.get_piece_is_white(condition_pos) == condition_pos_colour and
                    isinstance(self.__board_state[condition_pos[0]][condition_pos[1]], Pawn) and
                    self.__played_moves[-1][1] == condition_pos):
                    return True
        
        return False
            
        

    
    def draw(self, surface, select_colour=select_colour):
        selected_piece_coords = self.__BoardInput.get_selected_piece_coords()
        is_dragging = self.__BoardInput.get_is_dragging()
        
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
                    if not(is_dragging and selected_piece_coords == (i , j)):
                        self.__surface.blit(
                            pygame.transform.scale(
                                piece.image,
                                (self.__square_width, self.__square_width)
                            ),
                            square_coords
                        )
        
        # Draw highlighted square and valid moves from that piece
        if selected_piece_coords:
            highlight_rect = pygame.Rect(
                (
                    selected_piece_coords[1] * self.__square_width,
                    selected_piece_coords[0] * self.__square_width
                ),
                (
                    self.__square_width,
                    self.__square_width
                )
            )
            pygame.draw.rect(self.__surface, select_colour, highlight_rect, 2)
            
        

        if is_dragging:
            y, x = selected_piece_coords
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
        

class BoardInput:
    def __init__(self, board):
        self.__board = board
        self.__is_dragging = False
        self.__selected_piece_coords = None
        self.__selected_twice = False
    
    def get_is_dragging(self):
        return self.__is_dragging
    
    def get_selected_piece_coords(self):
        return self.__selected_piece_coords
        
    def __is_valid_piece_coords(self, coords):
        if coords == None or self.__board.get_piece(coords) == None:
            return False
        return True
    
    def click_down(self):
        coords = self.__board.get_mouse_square()
        if self.__is_valid_piece_coords(self.__board.get_mouse_square()):
            if coords == self.__selected_piece_coords:
                self.__selected_twice = True
            self.__selected_piece_coords = coords
            self.__is_dragging = True
            return
        
        self.__selected_piece_coords = None
            
        
    def click_up(self):
        self.__is_dragging = False
        new_selected_coords = self.__board.get_mouse_square()
        if new_selected_coords == None or self.__selected_piece_coords == None:
            self.__selected_piece_coords = None
        elif new_selected_coords != self.__selected_piece_coords:
            self.__board.move((self.__selected_piece_coords, new_selected_coords))
            self.__selected_piece_coords = None
        else:
            if self.__selected_twice:
                self.__selected_twice = False
                self.__selected_piece_coords = None
                
        
        
            
    
    def draw(self, *args, **kwargs):
        self.__board.draw(*args, **kwargs)
        

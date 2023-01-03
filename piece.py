from abc import ABCMeta, abstractmethod
from pygame import image


# Abstract piece class
class Piece(metaclass=ABCMeta):
    def __init__(self, colour, short_name, pos):
        self.__colour = colour
        self.__pos = pos
        self.image = image.load(f'Assets/PieceImages/{short_name}{colour}.png')
    
    def set_pos(self, pos):
        self.__pos = pos

    @abstractmethod
    def get_valid_moves(self):
        pass
    

class Queen(Piece):
    def __init__(self, colour, pos=None):
        super().__init__(colour, 'q', pos)

    def get_valid_moves(self):
        pass
        
                
class Rook(Piece):
    def __init__(self, colour, pos=None):
        super().__init__(colour, 'r', pos)

    def get_valid_moves(self):
        pass
        
        
class Knight(Piece):
    def __init__(self, colour, pos=None):
        super().__init__(colour, 'n', pos)

    def get_valid_moves(self):
        pass
        
        
class Bishop(Piece):
    def __init__(self, colour, pos=None):
        super().__init__(colour, 'b', pos)

    def get_valid_moves(self):
        pass
        
        
class King(Piece):
    def __init__(self, colour, can_castle_long=True, can_castle_short=True, pos=None):
        super().__init__(colour, 'k', pos)
        self.__can_castle_long = can_castle_long
        self.__can_castle_short = can_castle_short

    def get_valid_moves(self):
        pass
        
        
class Pawn(Piece):
    def __init__(self, colour, pos=None):
        super().__init__(colour, 'p', pos)
        self.__has_moved = False

    def get_valid_moves(self):
        y, x = self.__pos
        if self.__has_moved:
            if self.__colour == 'l':
                return set((y - 1, x))
            else:
                return set((y + 1, x))
        else:
            if self.__colour == 'l':
                return set((y - 1, x), (y - 2, x))
            else:
                return set((y + 1, x), (y + 2, x))
                

from abc import ABCMeta, abstractmethod
from pygame import image


# Abstract piece class
class Piece(metaclass=ABCMeta):
    def __init__(self, colour, short_name, pos):
        self.colour = colour
        self.is_white = True if colour == 'l' else False
        self.pos = pos
        self.image = image.load(f'Assets/PieceImages/{short_name}{colour}.png')
    
    def set_pos(self, pos):
        self.pos = pos
        
    def get_is_white(self):
        return self.is_white
        
    @abstractmethod
    def get_pseudo_moves(self):
        ...

# Abstract Restricted Piece class
class RestrictedPiece(Piece, metaclass=ABCMeta):
    def __init__(self, colour, short_name, pos, has_moved):
        super().__init__(colour, short_name, pos)
        self._has_moved = has_moved
    
    def get_has_moved(self):
        return self._has_moved
    
    def set_has_moved(self, has_moved):
        self._has_moved = has_moved
        

class Queen(Piece):
    def __init__(self, colour, pos=None):
        super().__init__(colour, 'q', pos)

    def get_pseudo_moves(self):
        moves = set()
        return moves
        
                
class Rook(RestrictedPiece):
    def __init__(self, colour, pos=None, has_moved=False):
        super().__init__(colour, 'r', pos, has_moved)

    def get_pseudo_moves(self):
        moves = []
        return moves
        
        
class Knight(Piece):
    def __init__(self, colour, pos=None):
        super().__init__(colour, 'n', pos)

    def get_pseudo_moves(self):
        moves = []
        return moves
        
        
class Bishop(Piece):
    def __init__(self, colour, pos=None):
        super().__init__(colour, 'b', pos)

    def get_pseudo_moves(self):
        moves = []
        return moves
        
        
class King(RestrictedPiece):
    def __init__(self, colour, pos=None, has_moved=False):
        super().__init__(colour, 'k', pos, has_moved)

    def get_pseudo_moves(self):
        moves = []
        return moves
        
        
class Pawn(RestrictedPiece):
    def __init__(self, colour, pos=None, has_moved=False):
        super().__init__(colour, 'p', pos, has_moved)

    def get_pseudo_moves(self):
        moves = []
        y, x = self.pos
        if self.is_white:
            moves.append(((y-1, x), None))
            moves.append(((y-1, x+1), False))
            moves.append(((y-1, x-1), False))
            moves.append(((y-1, x+1), None))
            moves.append(((y-1, x-1), None, (True, (y, x-1), False)))
            moves.append(((y-1, x+1), None, (True, (y, x+1), False)))
        else:
            moves.append(((y+1, x), None))
            moves.append(((y+1, x+1), True))
            moves.append(((y+1, x-1), True))
            moves.append(((y+1, x-1), None, (True, (y, x-1), True)))
            moves.append(((y+1, x+1), None, (True, (y, x+1), True)))
        
        if self._has_moved == False:
            if self.is_white:
                moves.append(((y-2, x), None))
            else:
                moves.append(((y+2, x), None))
        
        return moves
                

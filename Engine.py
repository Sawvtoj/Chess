'''
The brain behind the whole chess game
'''

class Brain():
    
    def __init__(self):
        
        '''
        B = Black
        Q = White
        R = Rook
        N = Knight
        B = Bishop
        Q = Queen
        K = King
        P = Pawn
        '  ' = Empty Space
        Board is a 2d 8x8 list representing the color piece and it's type
        '''
        self.board = [
            ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
            ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],    
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],  
            ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
        ]
        
        self.white_Turn = True
        self.move_Log = []
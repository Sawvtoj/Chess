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
        
    def make_Move(self, move):
        self.board[move.start_Row][move.start_Col] = '  '
        self.board[move.end_Row][move.end_Col] = move.piece_Moved
        self.move_Log.append(move)
        self.white_Turn = not self.white_Turn #change turns 

    def undo_Move(self):
        if len(self.move_Log) != 0:
            move = self.move_Log.pop()
            self.board[move.start_Row][move.start_Col] = move.piece_Moved
            self.board[move.end_Row][move.end_Col] = move.piece_Captured
            self.white_Turn = not self.white_Turn
            
    def get_Valid_Moves(self):
        return self.get_All_Possible_Moves()
    
    def get_All_Possible_Moves(self): 
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'W' and self.white_Turn) or (turn == 'B' and not self.white_Turn):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.get_Pawn_Moves(r, c, moves)
                    elif piece == 'R':
                        self.get_Rook_Moves(r, c, moves)
        return moves

    def get_Pawn_Moves(self, r, c, moves):
        pass
        
    def get_Rook_Moves(self, r, c, moves):
        pass
    
    def get_Bishop_Moves(self, r, c, moves):
        pass
    
    def get_Knight_Moves(self, r, c, moves):
        pass
    
    def get_Queen_Moves(self, r, c, moves):
        pass
    
    def get_King_Moves(self, r, c, moves):
        pass    
#####################################################################        
#####################################################################
##################################################################### 

       
class Move():
    
    ranks_To_Rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_To_Ranks = {v: k for k, v in ranks_To_Rows.items()}
    files_To_Cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_To_Files = {v: k for k, v in files_To_Cols.items()}
    
    def __init__(self, start_Sq, end_Sq, board):
        self.start_Row = start_Sq[0]
        self.start_Col = start_Sq[1]
        self.end_Row = end_Sq[0]
        self.end_Col = end_Sq[1]
        self.piece_Moved = board[self.start_Row][self.start_Col]
        self.piece_Captured = board[self.end_Row][self.end_Col]
        self.move_ID = self.start_Row * 1000 + self.start_Col * 100 + self.end_Row * 10 + self.end_Col
      
    #Overriding the equals method    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False
        
    def get_Chess_Notation(self):
        #Could change to real chess notation
        return self.get_Rank_File(self.start_Row, self.start_Col) + self.get_Rank_File(self.end_Row, self.end_Col)
        
    def get_Rank_File(self, r, c):
        return self.cols_To_Files[c] + self.rows_To_Ranks[r]
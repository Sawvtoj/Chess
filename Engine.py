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
        
        '''
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],    
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],  
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
        '''
        
        self.move_Functions = {'P': self.get_Pawn_Moves, 'R': self.get_Rook_Moves, 'N': self.get_Knight_Moves,
                               'B': self.get_Bishop_Moves, 'Q': self.get_Queen_Moves, 'K': self.get_King_Moves}
        
        self.white_Turn = True
        self.move_Log = []
        self.wKing_Location = (7, 4)
        self.bKing_Location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassant_Possible = ()
        self.enpassant_Possible_Log = [self.enpassant_Possible]
        self.current_Castling_Right = CastleRight(True, True, True, True)
        self.castle_Right_log = [CastleRight(self.current_Castling_Right.wks, self.current_Castling_Right.bks,
                                  self.current_Castling_Right.wqs, self.current_Castling_Right.bqs)]

        
    
                
    def make_Move(self, move):
        self.board[move.start_Row][move.start_Col] = '  '
        self.board[move.end_Row][move.end_Col] = move.piece_Moved
        self.move_Log.append(move)
        self.white_Turn = not self.white_Turn #change turns 
        
        #Update the King's Location
        if move.piece_Moved == 'WK':
            self.wKing_Location = (move.end_Row, move.end_Col)
        if move.piece_Moved == 'BK':
            self.bKing_Location = (move.end_Row, move.end_Col)
        
        if move.is_Pawn_Promotion:
            print(move.promotion_Choice)
            
            if move.promotion_Choice == 'Q':
                self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'Q'
            if move.promotion_Choice == 'B':
                self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'B'
            if move.promotion_Choice == 'N':
                self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'N'
            if move.promotion_Choice == 'R':
                self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'R'

                
            
        if move.is_Enpassant_Move:
            self.board[move.start_Row][move.end_Col] = '  ' 
        
        if move.piece_Moved[1] == 'P' and abs(move.start_Row - move.end_Row) == 2:
            self.enpassant_Possible = ((move.start_Row + move.end_Row)//2, move.start_Col)
        else:
            self.enpassant_Possible = ();
        
        if move.is_Castle_Move:
            if move.end_Col - move.start_Col == 2: #kingside castle move
                self.board[move.end_Row][move.end_Col - 1] = self.board[move.end_Row][move.end_Col + 1]
                self.board[move.end_Row][move.end_Col + 1] = '  '
            else: #queenside castle move
                self.board[move.end_Row][move.end_Col + 1] = self.board[move.end_Row][move.end_Col - 2]
                self.board[move.end_Row][move.end_Col - 2] = '  '
                
        self.enpassant_Possible_Log.append(self.enpassant_Possible)
        self.update_Castle_Right(move)
        self.castle_Right_log.append(CastleRight(self.current_Castling_Right.wks, self.current_Castling_Right.bks,
                                  self.current_Castling_Right.wqs, self.current_Castling_Right.bqs))    
        '''    
        if move.promotion_Choice != None:
            if move.promotion_Choice == 'Q':
                self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'Q'
        
       
        #Pawn Promotion
        if move.is_Pawn_Promotion:
            if self.promotion_Choice == 'Q':
                self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'Q'
            if self.promotion_Choice == 'R':
                self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'R'
            if self.promotion_Choice == 'B':
                self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'B'
            if self.promotion_Choice == 'N':
                self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'N'
        '''
                
    def undo_Move(self):
        if len(self.move_Log) != 0:
            move = self.move_Log.pop()
            self.board[move.start_Row][move.start_Col] = move.piece_Moved
            self.board[move.end_Row][move.end_Col] = move.piece_Captured
            self.white_Turn = not self.white_Turn
            
            #Update the King's Location
            if move.piece_Moved == 'WK':
                self.wKing_Location = (move.start_Row, move.start_Col)
            elif move.piece_Moved == 'BK':
                self.bKing_Location = (move.start_Row, move.start_Col)
                
            #undo en passant
            if move.is_Enpassant_Move:
                self.board[move.end_Row][move.end_Col] = '  '
                self.board[move.start_Row][move.end_Col] = move.piece_Captured
                
            self.enpassant_Possible_Log.pop()
            self.enpassant_Possible = self.enpassant_Possible_Log[-1]
            
            self.castle_Right_log.pop()
            new_Rights = self.castle_Right_log[-1]
            self.current_Castling_Right = CastleRight(new_Rights.wks, new_Rights.bks, new_Rights.wqs, new_Rights.bqs)
            
            if move.is_Castle_Move:
                if move.end_Col - move.start_Col == 2: #kingside castle move
                    self.board[move.end_Row][move.end_Col + 1] = self.board[move.end_Row][move.end_Col - 1]
                    self.board[move.end_Row][move.end_Col - 1] = '  '
                else: #queenside castle move
                    self.board[move.end_Row][move.end_Col - 2] = self.board[move.end_Row][move.end_Col + 1]
                    self.board[move.end_Row][move.end_Col + 1] = '  '
            
            self.checkmate = False
            self.stalemate = False
            
    def update_Castle_Right(self, move):
        if move.piece_Moved == 'WK':
            self.current_Castling_Right.wks = False
            self.current_Castling_Right.wqs = False
        
        elif move.piece_Moved == 'BK':
            self.current_Castling_Right.bks = False
            self.current_Castling_Right.bqs = False
        
        elif move.piece_Moved == 'WR':
            if move.start_Row == 7:
                if move.start_Col == 0:
                    self.current_Castling_Right.wqs = False
                elif move.start_Row == 7:
                    self.current_Castling_Right.wks = False
        
        elif move.piece_Moved == 'BR':
            if move.start_Row == 0:
                if move.start_Col == 0:
                    self.current_Castling_Right.bqs = False
                elif move.start_Row == 7:
                    self.current_Castling_Right.bks = False
                    
        if move.piece_Captured == 'WR':
            if move.end_Row == 7:
                if move.end_Col == 0:
                    self.current_Castling_Right.wqs = False
                elif move.end_Col == 7:
                    self.current_Castling_Right.wks = False
        elif move.piece_Captured == 'BR':
            if move.end_Row == 0:
                if move.end_Col == 0:
                    self.current_Castling_Right.bqs = False
                elif move.end_Col == 7:
                    self.current_Castling_Right.bks = False
                        
    def get_Valid_Moves(self):
        temp_Enpassant_Possible = self.enpassant_Possible
        temp_Castle_Rights = CastleRight(self.current_Castling_Right.wks, self.current_Castling_Right.bks,
                                  self.current_Castling_Right.wqs, self.current_Castling_Right.bqs)
        
        moves = self.get_All_Possible_Moves()
        
        if self.white_Turn:
            self.get_Castle_Moves(self.wKing_Location[0], self.wKing_Location[1], moves,)
        
        else:
            self.get_Castle_Moves(self.bKing_Location[0], self.bKing_Location[1], moves,)
        
        for i in range(len(moves)-1, -1, -1):
            
            self.make_Move(moves[i])
            
            self.white_Turn = not self.white_Turn
            
            if self.in_Check():                
                moves.remove(moves[i])            
            
            self.white_Turn = not self.white_Turn   #Switch back turn
            self.undo_Move()
        
        if len(moves) == 0: #Either checkmate or stalemate
            if self.in_Check():
                self.checkmate = True
                print('Checkmate')
            else:
                self.stalemate = True
                print('Stalemate')
        else:
            self.checkmate = False
            self.stalemate = False
        
        self.enpassant_Possible = temp_Enpassant_Possible
        self.current_Castling_Right = temp_Castle_Rights
        
        return moves
    
    def in_Check(self):
        if self.white_Turn:
            return self.square_Under_Attack(self.wKing_Location[0], self.wKing_Location[1])
        else:
            return self.square_Under_Attack(self.bKing_Location[0], self.bKing_Location[1])
    
    def square_Under_Attack(self, r, c):

        self.white_Turn = not self.white_Turn
        
        opp_Moves = self.get_All_Possible_Moves()
        
        self.white_Turn = not self.white_Turn   #Switch back turn

        for move in opp_Moves:
            if move.end_Row == r and move.end_Col == c: #Square is under attack
                return True
                
        return False
    
    def get_All_Possible_Moves(self): 
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'W' and self.white_Turn) or (turn == 'B' and not self.white_Turn):
                    piece = self.board[r][c][1]
                    self.move_Functions[piece](r, c, moves)
        return moves

    def get_Pawn_Moves(self, r, c, moves):
        if self.white_Turn:
            if self.board[r - 1][c] == '  ':
                moves.append(Move((r,c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == '  ': #Checks to see if the square in two squares in front of the pawn is empty
                    moves.append(Move((r, c), (r - 2, c), self.board))
            
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'B':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1, c-1) == self.enpassant_Possible:    
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, is_Enpassant_Move = True))
                    
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'B':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r-1, c+1) == self.enpassant_Possible:    
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, is_Enpassant_Move = True))
                    
        else:    
            if self.board[r + 1][c] == '  ': #Checks to see if the square in front of the pawn is empty
                moves.append(Move((r,c), (r + 1,c), self.board))
                if r == 1 and self.board[r + 2][c] == '  ': #Checks to see if the square in two squares in front of the pawn is empty
                    moves.append(Move((r, c), (r + 2, c), self.board))
            
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'W':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1, c-1) == self.enpassant_Possible:    
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, is_Enpassant_Move = True))
                    
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'W':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                    
                elif (r+1, c+1) == self.enpassant_Possible:    
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, is_Enpassant_Move = True))            
                    
    def get_Rook_Moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_Color = 'B' if self.white_Turn else 'W'
        
        for d in directions:
            for i in range(1, 8):
                end_Row = r + d[0] * i
                end_Col = c + d[1] * i
                
                if 0 <= end_Row < 8 and 0 <= end_Col < 8:
                    end_Piece = self.board[end_Row][end_Col]
                    if end_Piece == '  ':
                        moves.append(Move((r,c), (end_Row, end_Col), self.board))
                    elif end_Piece[0] == enemy_Color:
                        moves.append(Move((r, c), (end_Row, end_Col), self.board))
                        break
                    else:
                        break
                else:
                    break
    
    def get_Bishop_Moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_Color = 'B' if self.white_Turn else 'W'
        
        for d in directions:
            for i in range(1, 8):
                end_Row = r + d[0] * i
                end_Col = c + d[1] * i
                
                if 0 <= end_Row < 8 and 0 <= end_Col < 8:
                    end_Piece = self.board[end_Row][end_Col]
                    if end_Piece == '  ':
                        moves.append(Move((r,c), (end_Row, end_Col), self.board))
                    elif end_Piece[0] == enemy_Color:
                        moves.append(Move((r, c), (end_Row, end_Col), self.board))
                        break
                    else:
                        break
                else:
                    break
    
    def get_Knight_Moves(self, r, c, moves):
        #Up 2, 1 right or left
        #(-2, -1), (-2, 1)
        
        #Up 1, 2 right or left
        #(-1, -2), (-1, 2)
        
        #2 right or left, 1 down
        #(1, 2), (1, -2)
        
        #1 right or left, 2 down
        #(2, -1), (2, 1)
        
        knight_Moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1))
        ally_Color = 'W' if self.white_Turn else 'B'
        for n in knight_Moves:
            end_Row = r + n[0]
            end_Col = c + n[1]
            if 0 <= end_Row < 8 and 0 <= end_Col < 8:
                end_Piece = self.board[end_Row][end_Col]
                if end_Piece[0] != ally_Color:
                    moves.append(Move((r, c), (end_Row, end_Col), self.board))
        
    def get_Queen_Moves(self, r, c, moves):
        self.get_Rook_Moves(r, c, moves)
        self.get_Bishop_Moves(r, c, moves)
    
    def get_King_Moves(self, r, c, moves):
        king_Moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_Color = 'W' if self.white_Turn else 'B'
        for i in range(8):
            end_Row = r + king_Moves[i][0]
            end_Col = c + king_Moves[i][1]
            if 0 <= end_Row < 8 and 0 <= end_Col < 8:
                end_Piece = self.board[end_Row][end_Col]
                if end_Piece[0] != ally_Color:
                    moves.append(Move((r, c), (end_Row, end_Col), self.board))
        
        #self.get_Castle_Moves(r, c, moves, ally_Color)
        
    def get_Castle_Moves(self, r, c, moves):
        if self.square_Under_Attack(r, c):
            return
        if (self.white_Turn and self.current_Castling_Right.wks) or (not self.white_Turn and self.current_Castling_Right.bks):
            self.get_King_Side_Castle_Moves(r, c, moves)
        
        if (self.white_Turn and self.current_Castling_Right.wqs) or (not self.white_Turn and self.current_Castling_Right.bqs):
            self.get_Queen_Side_Castle_Moves(r, c, moves)
                    
    def get_King_Side_Castle_Moves(self, r, c, moves):
        if self.board[r][c + 1] == '  ' and self.board[r][c + 2] == '  ':
            if not self.square_Under_Attack(r, c + 1) and not self.square_Under_Attack(r, c + 2):
                moves.append(Move((r , c), (r, c + 2), self.board, is_Castle_Move = True))
        
    def get_Queen_Side_Castle_Moves(self, r, c, moves):
        if self.board[r][c - 1] == '  ' and self.board[r][c - 2] == '  ' and self.board[r][c - 3] == '  ':
            if not self.square_Under_Attack(r, c - 1) and not self.square_Under_Attack(r, c - 2):
                moves.append(Move((r , c), (r, c - 2), self.board, is_Castle_Move = True))      

#####################################################################        
#####################################################################
##################################################################### 

class CastleRight():
    
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        
       
class Move():
    
    ranks_To_Rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_To_Ranks = {v: k for k, v in ranks_To_Rows.items()}
    files_To_Cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_To_Files = {v: k for k, v in files_To_Cols.items()}
    
    def __init__(self, start_Sq, end_Sq, board, is_Enpassant_Move = False, is_Castle_Move = False, promotion_Choice = ' '):
        self.start_Row = start_Sq[0]
        self.start_Col = start_Sq[1]
        self.end_Row = end_Sq[0]
        self.end_Col = end_Sq[1]
        self.piece_Moved = board[self.start_Row][self.start_Col]
        self.piece_Captured = board[self.end_Row][self.end_Col]
        
        self.promotion_Choice = promotion_Choice
        self.is_Pawn_Promotion = ((self.piece_Moved == 'WP' and self.end_Row == 0) or (self.piece_Moved == 'BP' and self.end_Row == 7))   
                        
        self.is_Enpassant_Move = is_Enpassant_Move
        if self.is_Enpassant_Move:
            self.piece_Captured = 'WP' if self.piece_Moved == 'BP' else 'BP'        
        
        self.is_Castle_Move = is_Castle_Move
        
        self.move_ID = self.start_Row * 1000 + self.start_Col * 100 + self.end_Row * 10 + self.end_Col
      
    #Overriding the equals method    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False
        
    def get_Chess_Notation(self):
        #Could change to real chess notation
        return self.get_Rank_File(self.start_Row, self.start_Col) + self.get_Rank_File(self.end_Row, self.end_Col)
    
    def get_Promotion_Choice(self, move):    
        user_Choice = input('Queen: Q, Rook: R Bishop: B Knight: N - ')
        if user_Choice == 'Q':    
            move.promotion_Choice = 'Q'
            return move.promotion_Choice
        
        if user_Choice == 'R':
            move.promotion_Choice = 'R'
            return move.promotion_Choice
        
        if user_Choice == 'B':
            move.promotion_Choice = 'B'
            return move.promotion_Choice
        
        if user_Choice == 'N':
            move.promotion_Choice = 'N'
            return move.promotion_Choice
        
    def get_Rank_File(self, r, c):
        return self.cols_To_Files[c] + self.rows_To_Ranks[r]
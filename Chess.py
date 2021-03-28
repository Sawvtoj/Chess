import pygame as p
import Engine

WIDTH = HEIGHT = 512 #Size of window
DIMENSION = 8 #Dimension 
SQ_SIZE = HEIGHT // DIMENSION # size of chess board
MAX_FPS = 15 #for animations later on
IMAGES = {}


'''
Load the images once so no need to load and update the images per fram 
'''
def load_Images():
    piece_Images = ['WP', 'WR', 'WN', 'WB', 'WQ', 'WK', 'BQ', 'BK', 'BB', 'BN', 'BR', 'BP']
    for piece in piece_Images:
        IMAGES[piece] = p.transform.scale(p.image.load('ChessImages/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
        
def main():
    
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('White'))
    
    gs = Engine.Brain()
    valid_Moves = gs.get_Valid_Moves()
    move_Made = False
    animate = False
    
    load_Images()
    
    sq_Selected  = () #keeps track of the current selected square
    player_Clicks = [] #keeps track of where the user is clicking with the mouse button

    running = True
    game_Over = False
    
    while running:
        for e in p.event.get():
            
            if e.type == p.QUIT:
                running = False
                p.quit()
            
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_Over:
                    location = p.mouse.get_pos() #(x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                
                    if sq_Selected == (row, col): #if the user selected the same square
                        sq_Selected = () #reset
                        player_Clicks = [] #reset
                
                    else:
                        sq_Selected = (row, col)
                        player_Clicks.append(sq_Selected)
                
                    if len(player_Clicks) == 2:
                        move = Engine.Move(player_Clicks[0], player_Clicks[1], gs.board)
                        print(move.get_Chess_Notation())
                        print(move.is_Pawn_Promotion)
                        for i in range(len(valid_Moves)):
                            if move == valid_Moves[i]:
                                
                                
                                if move.is_Pawn_Promotion == True:
                                    print('Is Pawn Promtion')
                                    move.get_Promotion_Choice(valid_Moves[i])
                                        
                                    print(move.promotion_Choice)
                                    gs.make_Move(valid_Moves[i])     
                                    move_Made = True
                                    animate = True
                                    sq_Selected = ()
                                    player_Clicks = []
                                    
                                else:
                                    gs.make_Move(valid_Moves[i])     
                                    move_Made = True
                                    animate = True
                                    sq_Selected = ()
                                    player_Clicks = []
                                 
                        if not move_Made:
                            player_Clicks = [sq_Selected]
                   
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_Move()
                    move_Made = True
                    animate = False
                if e.key == p.K_r:
                    gs = Engine.Brain()
                    valid_Moves = gs.get_Valid_Moves()
                    sq_Selected = ()
                    player_Clicks = []
                    move_Made = False
                    animate = False
                    
        if move_Made:
            if animate:
                animate_Move(gs.move_Log[-1], screen , gs.board, clock)
            valid_Moves = gs.get_Valid_Moves()
            move_Made = False
            animate = False
            
        draw_Game_State(screen, gs, valid_Moves, sq_Selected)        
        
        if gs.checkmate:
            game_Over = True
            if gs.white_Turn:
                draw_Text(screen, 'Black Wins')
            else:
                draw_Text(screen, 'White Wins')
        elif gs.stalemate:
            game_Over = True
            draw_Text(screen, 'Stalemate')
        
        clock.tick(MAX_FPS)
        p.display.flip()
        
#Highlight the square selected and moves for piece selected
def highlight_Squares(screen, gs, valid_Moves, sq_Selected):
    if sq_Selected != ():
        r, c = sq_Selected
        if gs.board[r][c][0] == ('W' if gs.white_Turn else 'B'): #sq_Selected is a piece that can be moved
            
            #highlight the squares
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transperancy value if 0 transparent else 255 it is opaque
            s.fill(p.Color(0,100,0))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            
            #highlight moves from that square
            s.fill(p.Color(41,36,33))
            for move in valid_Moves:
                if move.start_Row == r and move.start_Col == c:
                    screen.blit(s, (move.end_Col * SQ_SIZE, move.end_Row * SQ_SIZE))
        
#Draw the board and updates it each move
def draw_Game_State(screen, gs, valid_Moves, sq_Selected):
    draw_Board(screen)
    highlight_Squares(screen, gs, valid_Moves, sq_Selected)
    draw_Pieces(screen, gs.board)
    
    
#Draw the board
def draw_Board(screen): 
    global colors
    colors = [p.Color('White'), p.Color(50, 205, 50)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
#Draw and updates the pieces
def draw_Pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "  ":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#Move Animation
def animate_Move(move, screen, board, clock):
    global colors
    dR = move.end_Row - move.start_Row
    dC = move.end_Col - move.start_Col
    framesPerSquare = 10 #frames to move one square
    frame_Count = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frame_Count + 1):
        r, c = move.start_Row + dR*frame/frame_Count, move.start_Col + dC*frame/frame_Count
        draw_Board(screen)
        draw_Pieces(screen, board)
        
        color = colors[(move.end_Row + move.end_Col) % 2]
        end_Square = p.Rect(move.end_Col * SQ_SIZE, move.end_Row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_Square)
        
        if move.piece_Captured != '  ':
            if move.is_Enpassant_Move:
                enpassant_Row = move.end_Row + 1 if move.piece_Captured[0] == 'B' else move.end_Row - 1
                end_Square = p.Rect(move.end_Col * SQ_SIZE, enpassant_Row * SQ_SIZE, SQ_SIZE, SQ_SIZE)

            screen.blit(IMAGES[move.piece_Captured], end_Square)
        
        screen.blit(IMAGES[move.piece_Moved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def draw_Text(screen, text):
    font = p.font.SysFont('Helvitca', 60, True, False)
    text_Object = font.render(text, 0, p.Color('Black'))
    text_Location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_Object.get_width()/2, HEIGHT/2 - text_Object.get_height()/2)
    screen.blit(text_Object, text_Location)
    text_Object = font.render(text, 0, p.Color(0, 100, 0))
    screen.blit(text_Object, text_Location.move(2, 2))

if __name__ == '__main__':
    main()
        
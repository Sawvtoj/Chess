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
    load_Images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
        
        draw_Game_State(screen, gs)        
                
        clock.tick(MAX_FPS)
        p.display.flip()
        
#Draw the board and updates it each move
def draw_Game_State(screen, gs):
    draw_Board(screen)
    
    draw_Pieces(screen, gs.board)
    
#Draw the board
def draw_Board(screen):   
    colors = [p.Color('Brown'), p.Color('Tan')]
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
    

if __name__ == '__main__':
    main()
        

from cProfile import run
import pygame as pg
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK","bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    
def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves() # get the valid move into list 
    moveMade = False # flag variable for when a move is made
    loadImages()
    running = True
    sqSelected = () # no square is selected, keep track of the last click of the user (row, col)
    playerClicks = [] # keep track of player clicks (two tuples : [(6,4), ()])
   
    while running:
        for e in pg.event.get() :
            if e.type == pg.QUIT:
                running = False
            # mouser handler
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos() # location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # the user clicked the same square
                    sqSelected = ()
                    playerClicks = [] #clear player click
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both 1st and 2nd
                if len(playerClicks) == 2: # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        validMoves = gs.getValidMoves()
                        sqSelected = () # reset user click
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]  
            # key handlers
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    gs.undoMove()
                    validMoves = gs.getValidMoves()
        # if moveMade:
        #     validMoves = gs.getValidMoves()
        #     print(validMoves)
        #     moveMade = False          
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()

#  Graphic
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [pg.Color("white"), pg.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
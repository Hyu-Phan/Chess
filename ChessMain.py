
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
    gameOver = False

    while running:
        for e in pg.event.get() :
            if e.type == pg.QUIT:
                running = False
            # mouser handler
            elif e.type == pg.MOUSEBUTTONDOWN:
                if not gameOver:
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
                            animateMove(gs.moveLog[-1], screen, gs.board, clock)
                            validMoves = gs.getValidMoves()
                            if len(validMoves) == 0:
                                gameOver = True
                            sqSelected = () # reset user click
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]  
            # key handlers
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    gs.undoMove()
                    validMoves = gs.getValidMoves()
                if e.key == pg.K_r: # reset the board 
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []


        # if moveMade:
        #     validMoves = gs.getValidMoves()
        #     print(validMoves)
        #     moveMade = False          
        drawGameState(screen, gs, validMoves, sqSelected)

        if gameOver:
            if gs.whiteToMove:
                drawText(screen, 'Black wins')
            else :
                drawText(screen, 'White wins')

        clock.tick(MAX_FPS)
        pg.display.flip()

#  Graphic
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # highlight selected square
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) 
            s.fill(pg.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

            #highlight moves
            s.fill(pg.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

                  
def drawBoard(screen):
    global colors
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


# Animating a move
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pg.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
        screen.blit(IMAGES[move.pieceMoved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        clock.tick(120)
     
def drawText(screen, text):
    font = pg.font.SysFont("Consolas", 32, True, False)
    textObject = font.render(text, 0 , pg.Color('red'))
    textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pg.Color('gray'))
    
    
if __name__ == "__main__":
    main()
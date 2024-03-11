from board import Board
import pygame, sys, os, math

# Initialize Pygame
pygame.init()

def x_Pos(position):
    return position % 8

def y_Pos(position):
    return math.floor(position/8)

def xy_Pos(position):
    x = x_Pos(position)
    y = y_Pos(position)
    return x, y

# -- -- -- -- -- --

def loadImages():
    imageDict = {}
    whiteDict = {}
    blackDict = {}

    whiteDict["Bishop"] = pygame.image.load("./piece_sprites/w-bishop.png")
    whiteDict["King"] = pygame.image.load("./piece_sprites/w-king.png")
    whiteDict["Knight"] = pygame.image.load("./piece_sprites/w-knight.png")
    whiteDict["Pawn"] = pygame.image.load("./piece_sprites/w-pawn.png")
    whiteDict["Queen"] = pygame.image.load("./piece_sprites/w-queen.png")
    whiteDict["Rook"] = pygame.image.load("./piece_sprites/w-rook.png")

    blackDict["Bishop"] = pygame.image.load("./piece_sprites/b-bishop.png")
    blackDict["King"] = pygame.image.load("./piece_sprites/b-king.png")
    blackDict["Knight"] = pygame.image.load("./piece_sprites/b-knight.png")
    blackDict["Pawn"] = pygame.image.load("./piece_sprites/b-pawn.png")
    blackDict["Queen"] = pygame.image.load("./piece_sprites/b-queen.png")
    blackDict["Rook"] = pygame.image.load("./piece_sprites/b-rook.png")

    imageDict["White"] = whiteDict
    imageDict["Black"] = blackDict

    return imageDict

# constants

PIECE_IMAGES = loadImages()
WIDTH, HEIGHT = 512, 512
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT // ROWS
LIGHT = (230, 230, 200)
DARK = (135, 170, 100)

class ChessPiece:
    def __init__(self, screen, pieceObject): # pieceobject : {"Piece": Piece, "Position": ##, "Color": "Black"}
        self.image = PIECE_IMAGES[pieceObject["Color"]][pieceObject["Piece"].type] # Piece Color -> Piece.type
        self.position = pieceObject["Position"]
        self.color = pieceObject["Color"]
        self.piece = pieceObject["Piece"]

        x, y = xy_Pos(self.position)
        self.x = x * SQUARE_SIZE
        self.y = y * SQUARE_SIZE

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Function to draw the chessboard
def draw_board(screen):
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(screen, LIGHT, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_sprites(screen, chessboard):
    chessPieceIndicies = chessboard.pieceObjects()


    return None



# Main function
def main():
    chessboard = Board()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('PyChess')
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(DARK)
        draw_board(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

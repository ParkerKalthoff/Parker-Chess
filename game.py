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

def loadImages():
    imageDict = {}
    whiteDict = {}
    blackDict = {}

    # Load white pieces
    whiteDict["Bishop"] = pygame.transform.scale(pygame.image.load("./piece_sprites/w-bishop.png"), (SQUARE_SIZE, SQUARE_SIZE))
    whiteDict["King"] = pygame.transform.scale(pygame.image.load("./piece_sprites/w-king.png"), (SQUARE_SIZE, SQUARE_SIZE))
    whiteDict["Knight"] = pygame.transform.scale(pygame.image.load("./piece_sprites/w-knight.png"), (SQUARE_SIZE, SQUARE_SIZE))
    whiteDict["Pawn"] = pygame.transform.scale(pygame.image.load("./piece_sprites/w-pawn.png"), (SQUARE_SIZE, SQUARE_SIZE))
    whiteDict["Queen"] = pygame.transform.scale(pygame.image.load("./piece_sprites/w-queen.png"), (SQUARE_SIZE, SQUARE_SIZE))
    whiteDict["Rook"] = pygame.transform.scale(pygame.image.load("./piece_sprites/w-rook.png"), (SQUARE_SIZE, SQUARE_SIZE))

    # Load black pieces
    blackDict["Bishop"] = pygame.transform.scale(pygame.image.load("./piece_sprites/b-bishop.png"), (SQUARE_SIZE, SQUARE_SIZE))
    blackDict["King"] = pygame.transform.scale(pygame.image.load("./piece_sprites/b-king.png"), (SQUARE_SIZE, SQUARE_SIZE))
    blackDict["Knight"] = pygame.transform.scale(pygame.image.load("./piece_sprites/b-knight.png"), (SQUARE_SIZE, SQUARE_SIZE))
    blackDict["Pawn"] = pygame.transform.scale(pygame.image.load("./piece_sprites/b-pawn.png"), (SQUARE_SIZE, SQUARE_SIZE))
    blackDict["Queen"] = pygame.transform.scale(pygame.image.load("./piece_sprites/b-queen.png"), (SQUARE_SIZE, SQUARE_SIZE))
    blackDict["Rook"] = pygame.transform.scale(pygame.image.load("./piece_sprites/b-rook.png"), (SQUARE_SIZE, SQUARE_SIZE))

    imageDict["White"] = whiteDict
    imageDict["Black"] = blackDict

    return imageDict


# Constants
WIDTH, HEIGHT = 512, 512
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT // ROWS
LIGHT = (230, 230, 200)
DARK = (135, 170, 100)
PIECE_IMAGES = loadImages()

class ChessPiece:
    def __init__(self, screen, pieceObject):
        self.image = PIECE_IMAGES[pieceObject["Color"]][pieceObject["Piece"].type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (pieceObject["Position"] % 8 * SQUARE_SIZE, math.floor(pieceObject["Position"] / 8) * SQUARE_SIZE)
        screen.blit(self.image, self.rect)

# Function to draw the chessboard
def draw_board(screen):
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(screen, LIGHT, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_sprites(screen, chessboard):
    pieces = chessboard.pieceObjects()
    for piece in pieces:
        ChessPiece(screen, piece)

def init_pieces(screen, chessboard):
    pieces = []
    for piece in chessboard.pieceObjects():
        pieces.append(ChessPiece(screen, piece))
    return pieces

# Main function
def main():
    chessboard = Board()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('PyChess')
    clock = pygame.time.Clock()

    running = True
    pieces = init_pieces(screen, chessboard)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(DARK)
        draw_board(screen)
        draw_sprites(screen, chessboard)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

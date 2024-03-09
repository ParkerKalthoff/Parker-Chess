from board import Board
import pygame
import sys, os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 512, 512
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT // ROWS
LIGHT = (230, 230, 200)
DARK = (135, 170, 100)
SPRITE_DIRECTORY = os.listdir("piece_sprites")


def loadImages():
    imageDict = {}
    for sprite in SPRITE_DIRECTORY:
        imageDict[sprite.rsplit(".png")[0]] = pygame.image.load(sprite)


class ChessPiece:
    def __init__(self, gameObject):
        self.image = image
        self.rect = image.get_rect(center=position)

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

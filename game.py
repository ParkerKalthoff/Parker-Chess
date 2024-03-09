from board import Board
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 512, 512
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT // ROWS
LIGHT = (230, 230, 200)
DARK = (135, 170, 100)

# Function to draw the chessboard
def draw_board(screen):
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(screen, LIGHT, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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

import pygame
import time


class Ball_Game():

    def __init__(self):
        super().__init__()
        pygame.init()
        # screen and screen settings
        self.screen_color = (255, 255, 255)
        self.screen = pygame.display.set_mode((500, 500))
        self.screen.fill(self.screen_color)
        pygame.display.set_caption('my game')

        # settings for blocks
        self.block_width = 100
        self.block_height = 20
        self.block_color = (0, 0, 0)

        # create blocks
        self.block1 = pygame.Rect(255, 255, self.block_width, self.block_height)
        self.block2 = pygame.Rect(255, 255, self.block_width, self.block_height)

        #block1 position
        self.block1.x = 200
        self.block1.y = 200

        #block2 position
        self.block2.x = 300
        self.block2.y = 300

        # control if the game is running
        self.game_on = True
    def run_game(self):
        while self.game_on:
            self.move_blocks()
            if self.block1.x == 550:
                self.game_on = False


    def draw_blocks(self):
        pygame.draw.rect(self.screen, self.block_color, self.block1)
        pygame.draw.rect(self.screen, self.block_color, self.block2)
        pygame.display.flip()

    def move_blocks(self):
        self.block1.x += 1
        self.block2.x += 1
        self.draw_blocks()


game = Ball_Game()
game.run_game()


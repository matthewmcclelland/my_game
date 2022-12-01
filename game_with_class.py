import pygame
import time
import sys


#screen settings
screen_color = (255, 255, 255)
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('my game')
screen.fill(screen_color)

#settings for blocks
block_width = 100
block_height = 20
block_color = (0, 0, 0)

#create blocks
block1 = pygame.Rect(255, 255, block_width, block_height)
block2 = pygame.Rect(255, 255, block_width, block_height)

block1.x = 200
block1.y = 200

block2.x = 100
block2.y = 450


# draw block on screen
pygame.draw.rect(screen, block_color, block1)
pygame.draw.rect(screen, block_color, block2)

pygame.display.flip()
time.sleep(3)


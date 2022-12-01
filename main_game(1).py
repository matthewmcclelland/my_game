import sys
import pygame
import time
import random

class Ball_Game():

    def __init__(self):
        super().__init__()
        pygame.init()
        # screen and screen settings
        self.screen_dimensions = (650, 650)
        self.screen_color = (255, 255, 255)
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        pygame.display.set_caption('my game')
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height

        # restart game screen
        self.restart_screen = pygame.display.set_mode(self.screen_dimensions)
        self.restart_screen_color = (0, 255, 0)
        self.restart_screen_rect = self.restart_screen.get_rect()
        self.block1_won_text = 'Block 1 won!!'
        self.block2_won_text = 'block 2 won!!'

        # difficulty screen
        self.difficulty_screen = pygame.display.set_mode(self.screen_dimensions)
        self.difficulty_screen_color = (255, 255, 255)
        self.difficulty_screen_rect = self.difficulty_screen.get_rect()

        # start screen
        self.start_screen = pygame.display.set_mode(self.screen_dimensions)
        self.start_screen_color = (255, 255, 255)
        self.start_screen_rect = self.start_screen.get_rect()

        # settings true for all buttons
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.button_width = 250
        self.button_height = 50
        self.font = pygame.font.SysFont(None, 48)

        # Creating the multiplayer button to start the game.
        self.multiplayer_button_rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self.multiplayer_button_rect.midright = (self.screen_width - 200, self.screen_height/2)
        self.multiplayer_text = "Multiplayer"
        self.multiplayer_button_msg_image = self.font.render(self.multiplayer_text, True, self.text_color, self.button_color)
        self.multiplayer_button_msg_image_rect = self.multiplayer_button_msg_image.get_rect()
        self.multiplayer_button_msg_image_rect.center = self.multiplayer_button_rect.center

        #creating the single player button to start the game
        self.single_player_button_rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self.single_player_button_rect.midleft = (200, self.screen_height/2)
        self.single_player_text = "Single Player"
        self.single_player_button_msg_image = self.font.render(self.single_player_text, True, self.text_color, self.button_color)
        self.single_player_button_msg_image_rect = self.single_player_button_msg_image.get_rect()
        self.single_player_button_msg_image_rect.center = self.single_player_button_rect.center

        # creating button to go back to the start screen
        self.restart_button_rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self.restart_button_rect.center = self.restart_screen_rect.center
        self.restart_button_text = "Play Again?"
        self.restart_button_msg_image = self.font.render(self.restart_button_text, True, self.text_color, self.button_color)
        self.restart_button_msg_image_rect = self.restart_button_msg_image.get_rect()
        self.restart_button_msg_image_rect.center = self.restart_button_rect.center

        # settings for blocks
        self.block_width = 100
        self.block_height = 20
        self.block_color = (0, 0, 0)

        # create blocks
        self.block1 = pygame.Rect(255, 255, self.block_width, self.block_height)
        self.block2 = pygame.Rect(255, 255, self.block_width, self.block_height)

        #ball settings
        self.ball_color = (0, 0, 0)
        self.ball_radius = 15
        self.ball_width = 15
        self.ball_speed_x = 2
        self.ball_speed_y = 2
        self.original_speed_x = 2
        self.original_speed_y = 2

        #ball position
        self.ball_x = self.screen_width/2
        self.ball_y = self.screen_height/2
        self.ball_pos = [self.ball_x, self.ball_y]

        #block1 position
        self.block1.x = 0
        self.block1.y = 0

        #block2 position
        self.block2.x = 0
        self.block2.y = self.screen_height - 20

        #derermine if the block is moving
        self.block1_right = False
        self.block1_left = False

        self.block2_right = False
        self.block2_left = False

        self.block1_boundary = False
        self.block2_boundary = False

        # let's program know if blocks have been hit
        self.block1_hit = False
        self.block2_hit = False

        # which block is allowed to hit the ball
        self.block1_turn = False
        self.block2_turn = True

        # let's program know who loss the game
        self.block1_loss = False
        self.block2_loss = False

        # number of times that each block has been hit
        self.block1_times_hit = 0
        self.block2_times_hit = 0

        # block speed
        self.block_speed = 3

        # control if the game is running
        self.game_on = False

        # control if you are on the start screen
        self.start_screen_condition = True
        self.restart_screen_condition = False

        #controls the state of the buttons
        self.single_player_button_clicked = False
        self.multiplayer_button_clicked = False
        self.restart_button_clicked = False

        # controls which type of mode you are playing
        self.multiplayer = False
        self.single_player = False

        # condition to control the starting timer
        self.timer_condition = True

        #computer block
        self.computer_block_x = 0
        self.computer_block_speed = 1
        self.computer_block_location_to_get_to = 0
        self.computer_block_right = False
        self.computer_block_left = False

    def run_game(self):

        while True:
            if not self.game_on and self.start_screen_condition == True:
                self.display_start_screen()
                self.check_events()
            if self.game_on:
                self.check_events()
                self.check_collision_with_blocks()
                self.bounce_ball_of_blocks()
                self.check_boundaries()
                self.check_ball_boundaries()
                self.move_blocks()
                self.set_hits_to_false()
                self.check_if_game_loss()
                self.timer()

            if not self.game_on and self.restart_screen_condition == True:
                self.display_restart_screen()
                self.check_events()

    def timer(self):

        if self.timer_condition:
            time.sleep(2)
            self.timer_condition = False


    def draw_blocks(self):
        self.screen.fill(self.screen_color)
        self.move_ball()
        pygame.draw.circle(self.screen, self.ball_color, self.ball_pos, self.ball_radius, self.ball_width)
        pygame.draw.rect(self.screen, self.block_color, self.block1)
        pygame.draw.rect(self.screen, self.block_color, self.block2)
        pygame.display.flip()



    def move_blocks(self):
        if self.single_player:
            self.move_computer_block()
        if self.block1_right and self.multiplayer:
            self.block1.x += 1*self.block_speed
        if self.block1_left and self.multiplayer:
            self.block1.x += -1*self.block_speed
        if self.block2_right:
            self.block2.x += 1*self.block_speed
        if self.block2_left:
            self.block2.x += -1*self.block_speed
        self.draw_blocks()

    def check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_keydown(event)
            if event.type == pygame.KEYUP:
                self.check_keyup(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_if_single_player_button_clicked(mouse_pos)
                self.check_if_restart_button_clicked(mouse_pos)
                self.check_if_multiplayer_button_clicked(mouse_pos)

    def check_if_multiplayer_button_clicked(self, mouse_pos):
        self.multiplayer_button_clicked = self.multiplayer_button_rect.collidepoint(mouse_pos)
        # set all variables back to their original settings and change game on condition

        if self.multiplayer_button_clicked and self.game_on == False and self.start_screen_condition == True:
            self.intialize_game_var()
            self.multiplayer = True
            self.multiplayer_button_clicked = False
            self.single_player = False

    def intialize_game_var(self):
        self.block1_times_hit = 0
        self.block2_times_hit = 0
        self.ball_x = self.screen_width / 2
        self.ball_y = self.screen_height / 2
        self.ball_pos = [self.ball_x, self.ball_y]
        self.block1.x = self.screen_width / 2 - self.block_width / 2
        self.block1.y = 0
        self.block2.x = self.screen_width / 2 - self.block_width / 2
        self.block2.y = self.screen_height - 20
        self.game_on = True
        self.start_screen_condition = False
        self.game_on = True
        self.timer_condition = True
        self.computer_block_left = False
        self.computer_block_right = False



    def check_if_single_player_button_clicked(self, mouse_pos):
        self.single_player_button_clicked = self.single_player_button_rect.collidepoint(mouse_pos)
        # set all variables back to their original settings and change game on condition
        if self.single_player_button_clicked and self.game_on == False and self.start_screen_condition == True:
            self.intialize_game_var()
            self.single_player = True
            self.single_player_button_clicked = False
            self.multiplayer = False

    def check_if_restart_button_clicked(self, mouse_pos):
        self.restart_button_clicked = self.restart_button_rect.collidepoint(mouse_pos)
        if self.restart_button_clicked and self.game_on == False and self.restart_screen_condition == True:
            self.start_screen_condition = True
            self.restart_button_clicked = False
            self.single_player_button_clicked = False
            self.restart_screen_condition = False
            self.single_player = False
            self.multiplayer = False


    def check_keydown(self, event):

        if event.key == pygame.K_RIGHT:
            self.block1_right = True
        if event.key == pygame.K_LEFT:
            self.block1_left = True
        if event.key == pygame.K_d:
            self.block2_right = True
        if event.key == pygame.K_a:
            self.block2_left = True
        if event.key == pygame.K_ESCAPE:
            sys.exit()

    def check_keyup(self, event):

        if event.key == pygame.K_RIGHT:
            self.block1_right = False
        if event.key == pygame.K_LEFT:
            self.block1_left = False
        if event.key == pygame.K_d:
            self.block2_right = False
        if event.key == pygame.K_a:
            self.block2_left = False

    def check_boundaries(self):
        if self.block1.x >= self.screen_width - self.block_width:
            self.block1_boundary = True
            self.block1.x = self.screen_width - self.block_width
        if self.block1.x <= -1:
            self.block1_boundary = True
            self.block1.x = 0
        if self.block2.x >= self.screen_width - self.block_width:
            self.block2_boundary = True
            self.block2.x = self.screen_width - self.block_width
        if self.block2.x <= -1:
            self.block2_boundary = True
            self.block2.x = 0

    def move_ball(self):
        if self.block2_times_hit < 1:
            self.ball_speed_y = 1
            self.ball_speed_x = 1
        else:
            self.ball_speed_y = self.original_speed_y
            self.ball_speed_x = self.original_speed_x

        self.ball_x = self.ball_x + self.ball_speed_x
        self.ball_y = self.ball_y + self.ball_speed_y
        self.ball_pos = [self.ball_x, self.ball_y]

    def check_ball_boundaries(self):
        if self.ball_x >= self.screen_width:
            self.ball_speed_x = self.ball_speed_x*-1
        if self.block2_hit:
            self.ball_speed_y = self.ball_speed_y*-1
        if self.ball_x <= 0:
            self.ball_speed_x = self.ball_speed_x*-1
        if self.block2_hit:
            self.ball_speed_y = self.ball_speed_y*-1

    def bounce_ball_of_blocks(self):
        if self.block1_hit:
            self.ball_speed_y = self.ball_speed_y * -1
        if self.block2_hit:
            self.ball_speed_y = self.ball_speed_y * -1

    def check_collision_with_blocks(self):
        if self.ball_x >= self.block1.x and self.ball_x <= self.block1.x + self.block_width:
            if self.ball_y <= self.block1.y + self.block_height and self.block1_turn:
                self.block1_hit = True
                self.block1_times_hit += 1
                self.block1_turn = False
                self.block2_turn = True

        if self.ball_x >= self.block2.x and self.ball_x <= self.block2.x + self.block_width:
            if self.ball_y >= self.block2.y - self.block_height and self.block2_turn:
                self.block2_hit = True
                self.block2_times_hit += 1
                self.block2_turn = False
                self.block1_turn = True

    def set_hits_to_false(self):
        self.block1_hit = False
        self.block2_hit = False

    def check_if_game_loss(self):
        if self.ball_y < 0:
            self.block1_loss = True
            self.game_on = False
            self.restart_screen_condition = True
        if self.ball_y > self.screen_height:
            self.block2_loss = True
            self.game_on = False
            self.restart_screen_condition = True

    def display_difficulty_screen(self):
        self.difficulty_screen.fill(self.difficulty_screen_color)
        self.display_hard_button()
        self.display_medium_button()
        self.display_easy_button()
        pygame.display.flip()

    def display_restart_screen(self):
        self.restart_screen.fill(self.restart_screen_color)
        self.display_restart_button()
        pygame.display.flip()


    def display_start_screen(self):
        self.start_screen.fill(self.start_screen_color)
        self.display_multiplayer_button()
        self.display_single_player_button()
        pygame.display.flip()


    def display_multiplayer_button(self):
        self.start_screen.fill(self.button_color, self.multiplayer_button_rect)
        self.start_screen.blit(self.multiplayer_button_msg_image, self.multiplayer_button_msg_image_rect)

    def display_restart_button(self):
        self.restart_screen.fill(self.button_color, self.restart_button_rect)
        self.restart_screen.blit(self.restart_button_msg_image, self.restart_button_msg_image_rect)

    def display_single_player_button(self):
        self.start_screen.fill(self.button_color, self.single_player_button_rect)
        self.start_screen.blit(self.single_player_button_msg_image, self.single_player_button_msg_image_rect)

    def computer_controlled_block(self):
        keep_moving_left = False
        keep_moving_right = False
        if self.ball_x < self.block1.x + self.block_width/2:
            keep_moving_right = True
        if self.ball_x > self.block1.x + self.block_width/2:
            keep_moving_left = True

        if self.ball_speed_x > 0 and keep_moving_left:
            self.computer_block_left = True
        if self.ball_speed_x < 0 and keep_moving_right:
            self.computer_block_right = True

    def move_computer_block(self):
        self.computer_controlled_block()
        if self.computer_block_left:
            self.block1.x += 1 * self.block_speed
            print('left')
            self.computer_block_left = False
        if self.computer_block_right:
            self.block1.x += -1 * self.block_speed
            print('right')
            self.computer_block_right = False



game = Ball_Game()
game.run_game()


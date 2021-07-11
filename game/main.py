# Bricks! - An Arkanoid clone
# Christophe Nau - July 2021
# Graphics from Breakout Game Tile Set Free From ImagineLabs.Rocks (http://www.imaginelabs.rocks)
# Sound effects generated with https://sfxr.me
# Ascii banner generated with  https://www.ascii-art-generator.org/

import pygame as pg
from games_utils import *
import random
import os
from settings import *
from player import Player
from ball import Ball
from brick import Brick
from level import Level

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")

class Game:
    # initialize game window, etc
    def __init__(self):
        # initialize pygame and create window
        # initialize pygame (always needed)
        pg.init()
        # initialize pygame (needed when using sounds in the pygame)
        pg.mixer.init()
        # game window
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        # tile of the game window
        pg.display.set_caption(GAMETITLE)
        # used to handle game speed and to ensure the game runs at the FPS we decide
        self.clock = pg.time.Clock()
        
        # get the system's font name that matches what we have in the game settings
        self.font_name = pg.font.match_font(FONT_NAME)
        
        # load assets 
        self.load_data()
        
        # actually start the game
        self.running = True

    def load_data(self):
        # set up assets folders
        self.game_dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.game_dir, "images")
        self.sound_dir = os.path.join(self.game_dir, "sounds")
        self.level_dir = os.path.join(self.game_dir, "levels")
                
        # load sprites from Spritesheet
        self.spritesheet = Spritesheet(os.path.join(self.img_dir, SPRITESHEET))
        
        # load background image
        self.background = pg.image.load(os.path.join(self.img_dir, BACKGROUND_IMAGE)).convert()
        self.background_default = self.background
        self.background_rect = self.background.get_rect()

        # sounds
        self.ping_sounds = [pg.mixer.Sound(os.path.join(self.sound_dir, 'ping.wav')),
                            pg.mixer.Sound(os.path.join(self.sound_dir, 'pong.wav'))]
        
        self.pow_sounds = [pg.mixer.Sound(os.path.join(self.sound_dir, 'powerUp0.wav')),
                            pg.mixer.Sound(os.path.join(self.sound_dir, 'powerUp1.wav'))]
        self.laser_sound = [pg.mixer.Sound(os.path.join(self.sound_dir, 'laser_shoot.wav'))]    
        
    # start a new game
    def new(self):
        # put all sprites in a group, so we can easily Update them and Draw (render) them
        self.all_sprites = pg.sprite.Group()
        # group for the balls
        self.ball_sprites = pg.sprite.Group()
        self.superball_sprites = pg.sprite.Group()
        # group for the bricks
        self.brick_sprites = pg.sprite.Group()
        # group for all power ups
        self.powerup_sprites = pg.sprite.Group()
        # group for all bullets
        self.bullet_sprites = pg.sprite.Group()
    
        # create a new player
        self.player = Player(self)
        
        # Score
        self.score = 0
        
        # Level (influences the bricks resistance)
        self.level = 1
        
        # maximum speed for the ball (is adjusted for each level)
        self.ball_minimum_speed = BALL_MINIMUM_SPEED
        
        # probability to get a power up when a brick is destroyed
        self.powerup_probability = POWERUP_PROBABILITY
        
        # create a new ball
        # move the ball a little off the player to avoid detecting a hit
        self.ball = Ball(self, self.player.rect.centerx, self.player.rect.top - 15, self.ball_minimum_speed)
        
        # create the brick wall
        #self.create_brick_wall()
        Level(self, 1)
  
        # actually start the game
        self.run()

    # called when the player loses a life or clears a level
    def clean_screen(self):
        # kill all balls
        for ball in self.ball_sprites:
            ball.kill()
        # kill all powerups
        for pow in self.powerup_sprites:
            pow.kill()
        # kill all the bullets 
        for bullet in self.bullet_sprites:
            bullet.kill()
                   
    # game loop
    def run(self):
        self.playing = True
        # as long as the game is playing
        while self.playing == True:
            # keep loop running at the right speed
            # eg. if the loop takes less than 1/FPS second, wait until 1/FPS second
            self.clock.tick(FPS)
            # check for events, update the sprites and draw them
            self.events()
            self.update()
            self.draw()
        
    # Game loop - updates
    def update(self):
        # all sprites are in a group. The line below is all we need in the Update section
        self.all_sprites.update()

        # check to see if the player touches the ball
        # hits contains all the balls that hit the player
        hits = pg.sprite.spritecollide(self.player, self.ball_sprites, False, False)
        for hit in hits:
            # the player caught the ball => make it bounce 
            self.score += 1
            self.ping_sounds[1].play()
            # move the ball up a few pixels to avoid multiple hits
            hit.rect.y -= 15
            hit.bounce("paddle")

        # check to see if the player catches a powerup
        hits = pg.sprite.spritecollide(self.player, self.powerup_sprites, False, False)
        for hit in hits:
            # the player caught the powerup 
            self.pow_sounds[1].play()
            #  => apply powerup's action
            hit.action()
            # remove the powerup
            hit.kill()

        # check for collisions between ball(s) and brick(s)
        # hits returns a dictionary whose key is the ball(s). The value of each key is the list of bricks hit by this specific ball 
        hits = pg.sprite.groupcollide(self.ball_sprites, self.brick_sprites, False, False)          
        for hit in hits:
            self.score += 10
            # make the ball bounce
            hit.bounce("brick")
            # apply necessary actions to the brick that was hit
            for brick in hits[hit]:
                brick.hit("ball")
                                    
        # check for collisions between laser(s) and brick(s)
        hits = pg.sprite.groupcollide(self.bullet_sprites, self.brick_sprites, True, False)          
        for hit in hits:
            self.score += 10

            # apply necessary actions to the brick that was hit
            for brick in hits[hit]:
                brick.hit("laser")
        
        # if all the bricks have been destroyed
        if len(self.brick_sprites) == 0:
            # remove all bullets, powers and balls
            self.clean_screen()

            self.level += 1
            self.player.init()
            
            # go on to next level
            #self.create_brick_wall()
            # reset the backgroud in case there is none set for the next level
            self.background = self.background_default
            Level(self, self.level)
        
        
                
        # Game Over
        if self.player.lives == 0:
            #print("You lost !")
            self.playing = False
            #self.running = False
             
            
    # wait for player to press a key
    def wait_for_key(self):
        waiting = True
        while waiting:
            # static screen, don't need to run at a high FPS
            self.clock.tick(10)

            # wait for user's action
            for event in pg.event.get():
                # if the user closes the game window => end the waiting loop and the game
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                # if the user presses any key, end the waiting loop
                if event.type == pg.KEYUP:
                    waiting = False

        
    # Game loop - events
    def events(self):
        for event in pg.event.get():
            # check for closing the window
            if event.type == pg.QUIT:
                # stop the game
                # otherwise clicking on the red cross will not close the window
                if self.playing:
                    self.playing = False
                    self.running = False
            # spawn a new ball
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN: # pg.K_c:
                    Ball(self, self.player.rect.centerx + 5, self.player.rect.top - 5, self.ball_minimum_speed)
                    
    # Game loop - draw
    def draw(self):
        # use BLACK background in case the image is to small
        self.screen.fill(BLACK)
        # background image
        self.background_alpha = self.background.copy()
        alpha = 96
        self.background_alpha.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)
        self.screen.blit(self.background_alpha, self.background_rect)
        # all sprites are in a group. The line below is all we need in the Draw section
        self.all_sprites.draw(self.screen)

        # display player's score (after sprites so score is on top)
        self.draw_text(self.screen, "Score: " + str(self.score), 22, WHITE, WIDTH / 2, 5)

        # display player's remaining lives
        self.draw_text(self.screen, "Lives: " + str(self.player.lives), 22, WHITE, WIDTH, 5, "right")

        # display current level
        self.draw_text(self.screen, "Level: " + str(self.level), 22, WHITE, 5, 5, "left")

        # displaying things on screen is a super slow process => do it only at the very end
        # once everything is ready to be displayed
        # *after* drawing everything, flip the display
        pg.display.flip()
        
        
    # splash (entry) screen
    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "Bricks!", 64, WHITE, WIDTH / 2, HEIGHT / 4)
        #self.draw_text(self.screen, "Highscore: " + str(self.highscore) + " (Level " + str(self.highlevel).strip() + ")", 24, WHITE, WIDTH / 2, HEIGHT / 4 + 64)
        self.draw_text(self.screen, "Arrow keys move, Space to fire, Return to launch the ball", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to start", 18, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        
        pg.display.flip()
        
        self.wait_for_key()
        
        
    # Game over screen
    def show_go_screen(self):
        # if the user closes the game window, don't display the game over screen (otherwise the game won't quit) 
        if not self.running:
            return
        
        # stop the game's music
        pg.mixer.music.fadeout(500)
        # play the game over music
        pg.mixer.music.load(os.path.join(self.sound_dir, "hard_times.ogg"))
        pg.mixer.music.play(loops=-1)
            
        # display background image
        self.screen.blit(self.background, self.background_rect)
        
        self.draw_text(self.screen, "Game Over!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
        
        # did we beat the highscore ?
        '''
        if self.score > int(self.highscore):
            self.highscore = self.score
            self.draw_text(self.screen, "NEW HIGH SCORE !", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 20)
            with open(os.path.join(self.game_dir, HIGHSCORE_FILE), 'w') as f:
                f.write(str(self.score)+","+str(self.level))
        else:
            self.draw_text(self.screen, "High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 20)
        '''
        
        # display all graphical elements of the GO screen
        pg.display.flip()
        
        # wait for the user to press a key 
        self.wait_for_key()
        
        # stop the game over music
        pg.mixer.music.fadeout(500)
        

    # method to draw text
    # x, y: coordinates of the text to write
    # edge: left | right | middletop (default): which edge of the text box the coordinates apply to
    def draw_text(self, surf, text, size, color, x, y, edge="midtop"):
        font = pg.font.Font(self.font_name, size)
        # generate a surface to generate the text on to
        # True for anti-aliasing
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        # position the text
        if edge == "left":
          text_rect.left = x + 5
          text_rect.y = y
        elif edge == "right":
          text_rect.right = x - 5
          text_rect.y = y
        else:
          text_rect.midtop = (x, y)

        surf.blit(text_surface, text_rect)

        
if __name__  == "__main__":
    g = Game()
    g.show_start_screen()
    
    while g.running:
        g.new()
        g.show_go_screen()
    
    # end of the game loop => quit game
    print("thank you for playing that game")
    pg.quit() 
        
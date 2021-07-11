import pygame as pg
from settings import *
import random
import os
from bullet import Bullet
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        
        pg.sprite.Sprite.__init__(self, self.groups)
        # pass an instance of the Game to the player, so he knows about all the game variables
        self.game = game
        

        # number of remaining lives
        self.lives = 3
        # change this to resize the paddle 
        self.width_factor = 1
        # the paddle can't shoot until it caught a 'laser' powerup
        self.laser_enabled = False
        self.laser_strength = 1
        # how long do we wait between firing 2 consecutive times (ms)
        self.laser_shoot_delay = SHOOT_DELAY
        self.laser_last_shot = pg.time.get_ticks()

        self.load_images()
        if self.laser_enabled:
            self.image = self.paddle_laser_images[0]
        else:
            self.image = self.paddle_images[0]
        #self.image.set_colorkey(BLACK)
        # postion the player at the bottom of the screen
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 20)
        self.pos = vec(WIDTH // 2, HEIGHT - 20)
        
        # the player can only move left to right
        # we use vectors, just to reuse the code easily
        self.speed = vec(0,0)
        # player's acceleration
        self.acc = vec(0,0)
        # player's max accelaration
        self.max_acceleration = PLAYER_ACC
        # friction limits speed
        self.friction = PLAYER_FRICTION
        

        
        # start the animation
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        # paddle resizes animation
        self.last_resize = pg.time.get_ticks()
        # how quickly the animation goes
        self.frame_rate = 50
    
    def load_images(self):
        # images for the paddle
        self.paddle_images = [
                self.game.spritesheet.get_image(1158, 462, 243, 64),
                self.game.spritesheet.get_image(1158, 528, 243, 64),
                self.game.spritesheet.get_image(1158, 594, 243, 64)
            ]

        self.paddle_laser_images = [
            self.game.spritesheet.get_image(1158, 660, 243, 64),
            self.game.spritesheet.get_image( 839, 846, 243, 64),
            self.game.spritesheet.get_image( 772, 780, 243, 64)
            ]
        
        for i in range(len(self.paddle_images)):
            self.paddle_images[i].set_colorkey(BLACK)
            self.paddle_laser_images[i].set_colorkey(BLACK)
            self.paddle_images[i] = pg.transform.scale(self.paddle_images[i], (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.paddle_laser_images[i] = pg.transform.scale(self.paddle_laser_images[i], (PLAYER_WIDTH, PLAYER_HEIGHT))

            
    # initialize the player's properties after he died
    def init(self):
        self.width_factor = 1
        self.max_acceleration = PLAYER_ACC
        self.laser_enabled = False
        self.laser_strength = 1
                
    # resize the paddel with a smooth animation
    def resize(self):
        now = pg.time.get_ticks()
        width = self.rect.width
        if self.width_factor < 0.5:
            self.width_factor = 0.5
        if self.width_factor > 2:
            self.width_factor = 2            
        width_target = PLAYER_WIDTH * self.width_factor
        
        if now - self.last_resize > self.frame_rate:
        #if now - self.last_resize > 2000:
            self.last_resize = now        
            if width < width_target:
                # increase size
                width = width + 5
                if width >= width_target:
                    width = width_target
            else:
                # decrease size
                width = width - 5
                if width <= width_target:
                    width = width_target
            # reset the image otherwise, after a while the image looks weird
            if self.laser_enabled:
                self.image = self.paddle_laser_images[0]
            else:
                self.image = self.paddle_images[0]
            self.image = pg.transform.scale(self.image, (int(width), PLAYER_HEIGHT))
            self.rect = self.image.get_rect()  
                

    # shoot the laser
    def shoot(self):
        # only shoot if the laser has been enabled and if at least one ball is on the screen
        if self.laser_enabled and len(self.game.ball_sprites) > 0:
            now = pg.time.get_ticks()
            if now - self.laser_last_shot > self.laser_shoot_delay:
                self.laser_last_shot = now
                self.game.laser_sound[0].play()
                #if self.rect.centerx == 30 and self.rect.top == 0:
                bullet = Bullet(self.game, self.rect.centerx - self.rect.width // 2, self.rect.top - 10)            
                bullet = Bullet(self.game, self.rect.centerx + self.rect.width // 2 - 10, self.rect.top - 10)

    def update(self):
        # resize the paddle to its factor_size
        self.resize()
                 
        # player stays still unless a key is pressed
        # its acceleration is 0
        self.acc = vec(0,0)
        
        # get a list of all key(s) pressed
        keystate = pg.key.get_pressed()
        # if left arrow is pressed
        if keystate[pg.K_LEFT]:
            self.acc.x = -self.max_acceleration
        if keystate[pg.K_RIGHT]:
            self.acc.x = self.max_acceleration
        # keep on firing as long as the space bar is pressed
        if keystate[pg.K_SPACE]:
            self.shoot()
        
        # equations of motion
        # adjust acceleration by friction
        # the faster we go, the more friction there is
        self.acc += self.speed * self.friction
        # how acceleration affects speed
        self.speed += self.acc
        self.pos += self.speed + 0.5 * self.acc
                        
        # don't move over screen edges
        #if self.pos.x < (self.rect.width // 2):
        if self.pos.x < (self.rect.width // 2):
            self.pos.x = (self.rect.width // 2)
            #self.acc = vec(0,0)
            #self.speed = vec(0,0)
        if self.pos.x > WIDTH - (self.rect.width // 2):
            self.pos.x = WIDTH - (self.rect.width // 2)      
            #self.acc = vec(0,0)
            #self.speed = vec(0,0)
            
        self.rect.center = self.pos
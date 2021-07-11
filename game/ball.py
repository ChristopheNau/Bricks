import pygame as pg
from settings import *
import random
import os
vec = pg.math.Vector2

class Ball(pg.sprite.Sprite):
    def __init__(self, game, x, y, minimum_speed, type="normal"):
        self.groups = game.all_sprites, game.ball_sprites
        
        pg.sprite.Sprite.__init__(self, self.groups)
        # pass an instance of the Game to the player, so he knows about all the game variables
        self.game = game
        self.x = x
        self.y = y
        self.minimum_speed = minimum_speed
        # check maximum_speed > minumum speed otherwise, the randint() later on fails
        if self.minimum_speed > BALL_MAXIMUM_SPEED:
            self.minimum_speed = BALL_MAXIMUM_SPEED
        
        # speed.y must be < 0, so the ball goes up at first
        rsx = random.randrange(self.minimum_speed, BALL_MAXIMUM_SPEED)
        rsy = random.randrange(self.minimum_speed, BALL_MAXIMUM_SPEED)
        self.speed = vec(rsx, rsy)
        
        self.load_images()

        # how many damage points does the ball make to the bricks
        # special balls have more power
        self.type = type
        if self.type == "special":
            self.strength = 3
            self.image = self.ball_special_image
            self.image.set_colorkey(BLACK)
        else:
            self.strength = 1
            self.image = self.ball_images[0]
            self.image.set_colorkey(BLACK)
                
        # postion the ball on the player
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.x, self.y)

    def load_images(self):
        self.ball_images = [
            self.game.spritesheet.get_image(1403, 652, 64, 64, 4)
            ]
        self.ball_special_image = pg.image.load(os.path.join(self.game.img_dir, "specialball.png")).convert()
        self.ball_special_image = pg.transform.scale(self.ball_special_image, (16, 16))
        
    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
        # bounce on the screen edges
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed.x *= -1
        if self.rect.y < 0:
            self.speed.y *= -1       
        
        # kill the ball if it goes below the player
        if self.rect.top > HEIGHT:
            self.kill()
            # player loses a life
            if len(self.game.ball_sprites) == 0:
                self.game.player.lives -= 1
                self.game.player.init()
                self.game.clean_screen()
                
            
    def bounce(self, bounce_against):
        # special balls go throw all bricks
        # they only bounce against the paddle
        if bounce_against == "brick" and self.type == "special":
            return
        else:
            # invert vertical speed (make the ball go back up)
            self.speed.y *= -1

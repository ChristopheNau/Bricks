import pygame as pg
from settings import *
import random
import os
from ball import Ball

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerup_sprites
        
        pg.sprite.Sprite.__init__(self, self.groups)
        # pass an instance of the Game to the player, so he knows about all the game variables
        self.game = game
        self.x = x
        self.y = y
        
        self.load_images()
        self.type = random.choice(list(self.powerup_images.keys()))
        self.image = self.powerup_images[self.type]
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y

    def load_images(self):
        self.powerup_images = {
            "life"          : self.game.spritesheet.get_image(1637, 652,  64, 58, 4),
            "shrink"        : self.game.spritesheet.get_image(1158, 198, 243, 64, 4),
            "expand"        : self.game.spritesheet.get_image(1158, 264, 243, 64, 4),
            "laser"         : self.game.spritesheet.get_image(1158, 330, 243, 64, 4),
            "100pts"        : self.game.spritesheet.get_image(1084, 846, 243, 64, 4),
            "250pts"        : self.game.spritesheet.get_image(1403,   0, 243, 64, 4),
            "500pts"        : self.game.spritesheet.get_image(1329, 924, 243, 64, 4),
            "slow"          : self.game.spritesheet.get_image(1158,  66, 243, 64, 4),
            "fast"          : self.game.spritesheet.get_image( 349, 910, 243, 64, 4),
            "balls"         : self.game.spritesheet.get_image( 594, 910, 243, 64, 4),
            "specialball"   : self.game.spritesheet.get_image(1262, 726, 243, 64, 4)

        }
        
        # make backgroup transparent
        for f in self.powerup_images:
            self.powerup_images[f].set_colorkey(BLACK)
            #self.powerup_images[f] = pg.transform.scale(self.powerup_images[f], (BRICK_WIDTH, BRICK_HEIGHT))
        
    # what to do when the player caught a powerup
    def action(self):
        # extra life
        if self.type == "life":
            self.game.player.lives += 1
        # shrink the pladdle's width
        if self.type == "shrink":
            self.game.player.width_factor = 0.5
        # expand the paddle's width    
        if self.type == "expand":
            self.game.player.width_factor = 2
        if self.type == "laser":
            self.game.player.laser_enabled = True
            self.game.player.laser_strength += 1
        if self.type == "100pts" or self.type == "250pts" or self.type == "500pts":
            self.game.score += int(self.type.replace("pts", ""))
        # slow down the balls
        # don't slow it down too much otherwise it won't move any more
        if self.type == "slow":
            for b in self.game.ball_sprites:
                b.speed.x *= 0.75
                if b.speed.x < 0. and b.speed.x > -1:
                   b.speed.x = -1
                if b.speed.x > 0 and b.speed.x < 1:
                    b.speed.x = 1
                     
                b.speed.y *= 0.75
                if b.speed.y < 0. and b.speed.y > -1:
                   b.speed.y = -1
                if b.speed.y > 0 and b.speed.y < 1:
                    b.speed.y = 1
        # speed up the paddle
        if self.type == "fast":
            self.game.player.max_acceleration *= 1.1
            if self.game.player.max_acceleration > 1.5:
                self.game.player.max_acceleration = 1.5
        # multiple balls
        if self.type == "balls":
            for i in range(NUM_MULTIPLE_BALLS):
                x = random.randint(self.game.player.rect.centerx - self.game.player.rect.width, self.game.player.rect.centerx + self.game.player.rect.width)
                Ball(self.game, x, self.game.player.rect.top - 5, self.game.ball_minimum_speed)
        # special ball
        if self.type == "specialball":
            Ball(self.game, self.game.player.rect.centerx + 5, self.game.player.rect.top - 5, self.game.ball_minimum_speed, "special")
                
    
    def update(self):
        self.rect.y += 1
    
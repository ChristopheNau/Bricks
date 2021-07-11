import pygame as pg
from settings import *
import random
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        
        pg.sprite.Sprite.__init__(self, self.groups)
        # pass an instance of the Game to the player, so he knows about all the game variables
        self.game = game
        
        self.image = pg.Surface((60,10))
        self.image.fill(GREEN)
        
        # postion the player at the bottom of the screen
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 20)
        self.pos = vec(WIDTH // 2, HEIGHT - 20)
        
        # the player can only move left to right
        # we use vectors, just to reuse the code easily
        self.speed = vec(0,0)
        # player's acceleration
        self.acc = vec(0,0)
        
        self.balls = 3
    
    def update(self):
        # player stays still unless a key is pressed
        # its acceleration is 0
        self.acc = vec(0,0)
        
        # get a list of all key(s) pressed
        keystate = pg.key.get_pressed()
        # if left arrow is pressed
        if keystate[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keystate[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        # equations of motion
        # adjust acceleration by friction
        # the faster we go, the more friction there is
        self.acc += self.speed * PLAYER_FRICTION
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


class Ball(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.ball_sprites
        
        pg.sprite.Sprite.__init__(self, self.groups)
        # pass an instance of the Game to the player, so he knows about all the game variables
        self.game = game
        self.x = x
        self.y = y
        
        #self.speed = vec(5,-5)
        self.speed = vec(random.randint(2,5), random.randrange(2,5))
        
        self.image = pg.Surface((10,10))
        self.image.fill(WHITE)
        # make it transparent
        #self.image.set_colorkey(WHITE)
                
        # postion the ball on the player
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = vec(self.x, self.y)
        
    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
        # draw a circle
        pg.draw.circle(self.image, WHITE, (self.rect.x, self.rect.y), 10, 0)
        
        # bounce on the screen edges
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed.x *= -1
        if self.rect.y < 0:
            self.speed.y *= -1       
        
        # kill the ball if it goes below the player
        if self.rect.y > HEIGHT:
            self.kill()
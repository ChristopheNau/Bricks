# game settings
import random

WIDTH = 800
HEIGHT = 600
# game will be updated 'FPS' times per second
FPS = 60 
GAMETITLE = "Bricks - An Arkanoid clone"
FONT_NAME = "arial"
BACKGROUND_IMAGE = "background.png"
SPRITESHEET = "Breakout_Tile_Free.png"
# define useful colors
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
YELLOW    = (255, 255,   0)
BLUEGREEN = (  0, 155, 155)
SKYBLUE   = (135, 206, 235)
GOLD      = (255, 215,   0)

ALL_COLORS = [WHITE, BLACK, RED, GREEN, BLUE, YELLOW, BLUEGREEN, SKYBLUE, GOLD]

# Player's properties
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.10
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 20
SHOOT_DELAY = 250

# Bricks properties
BRICK_HEIGHT = 25
BRICK__VERTICAL_PADDING = 5
MININUM_TOP_PADDING = 50

# Probability to get a power up (%)
POWERUP_PROBABILITY = 5
# number of balls for the powerup "balls"
NUM_MULTIPLE_BALLS  = 3
# maximum speed a ball can achieve
BALL_MAXIMUM_SPEED = 7
BALL_MINIMUM_SPEED = 2
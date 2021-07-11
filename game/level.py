'''
This class is used to generate the pattern of the brick walls
'''
import pygame as pg
import os
from settings import *
from brick import Brick
# dictionary with all levels' properties (metadata and map)
import levels.all_levels as L

class Level(pg.sprite.Sprite):
    def __init__(self, game, level):
        # pass an instance of the Game to the player, so he knows about all the game variables
        self.game = game

        # get level's properties
        # if not set, used default
        try:
            current_level = L.levels[str(level)]
        except KeyError:
            # no entry for this level in levels => use the default one
            current_level = L.levels["default"]
        
        # change backrgound if "background_image" is set in the level's metadata
        try:
            self.game.background = pg.image.load(os.path.join(self.game.img_dir, current_level["metadata"]["background_image"])).convert()
            self.game.background_rect = self.game.background.get_rect()
        except KeyError:
            pass

        # set player's friction if "player_friction" is set in the level's metadata
        # use default value otherwise
        try:
            self.game.player.friction = current_level["metadata"]["player_friction"]
        except KeyError:
            self.game.player.friction = PLAYER_FRICTION

        # set ball's maximum speed if "max_ball_speed" is set in the level's metadata
        # use default value otherwise
        try:
            self.game.ball_minimum_speed = current_level["metadata"]["min_ball_speed"]
        except KeyError:
            self.game.ball_minimum_speed = BALL_MINIMUM_SPEED

        # set the probabily to get a power up if "powerup_probability" is set in the level's metadata
        # use default value otherwise
        try:
            self.game.powerup_probability = current_level["metadata"]["powerup_probability"]
        except KeyError:
            self.game.power_probability = POWERUP_PROBABILITY
            
        # create the bricks following the structure defined in "map" in the "all_levels.levels" dictionary
        row_nb = 0
        for row in current_level["map"]:
            #print(f"row # {row_nb} - {len(row)}")
            brick_width = int(WIDTH / (len(row) * 1.5))
            brick_height = int((HEIGHT - 2 * MININUM_TOP_PADDING) / (len(current_level["map"]) * 2.5))
            if brick_height > BRICK_HEIGHT:
                brick_height = BRICK_HEIGHT
            brick_padding = int(brick_width / 2)
            pos_x = (WIDTH - (len(row) * brick_width + (len(row) - 1) * brick_padding)) // 2
            pos_y = MININUM_TOP_PADDING + row_nb * (brick_height + BRICK__VERTICAL_PADDING)
            for tile in row:
                # the current tile is a brick to add
                if tile[0] > 0:
                    #print(f"Create a brick: width:{brick_width} height: {brick_height}- strength={tile[0]} - color={tile[1]} - x:{pos_x} - y:{pos_y}")
                    # if we don't have a specific level defined, use the default one but increase the bricks' strength
                    if level > len(L.levels) - 1:
                        brick_strength = int(tile[0]) + level
                    else:
                        brick_strength = tile[0]
                    b = Brick(self.game, brick_width, brick_height, brick_strength, tile[1])
                    b.rect.x = pos_x
                    b.rect.top = pos_y
                pos_x += brick_width + brick_padding
            row_nb += 1


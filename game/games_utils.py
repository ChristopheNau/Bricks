import pygame as pg

# utility class for loading and parsing spritesheets
class Spritesheet:
    def __init__(self, filename):   
        # load the image and convert it to a format pygame can easily manipulate (without .convert() the game would be slower)
        self.spritesheet = pg.image.load(filename).convert()
    
    # grab an image out of a larger spritesheet
    def get_image(self, x, y, width, height, resize_factor=1):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # resize the image
        # the (width, height) of new size must be integers 
        image = pg.transform.scale(image, (round(width / resize_factor), round(height / resize_factor)))
                
        return image
        
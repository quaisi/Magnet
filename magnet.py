#
# Magnets game
#
#

import pygame
from pygame.locals import *
import random

SCREENRECT = Rect(0,0,640,480)



class Sprite:
   """
The base Sprite class for creating / moving around characters
   
   Polarity is boolean - 
      True = Positive
      False = Negative
      
   """
   def __init__(self, xpos, ypos, polarity, filename):
      self.x = xpos
      self.y = ypos
      self.bitmap = image.load(filename).convert()
      self.bitmap.set_colorkey((255,0,255))
      self.xmoveamount = random.randint(-3, 3)
      self.ymoveamount = random.randint(1,3)

   def set_position(self, xpos, ypos):
      self.x = xpos
      self.y = ypos

   def render(self):
      screen.blit(self.bitmap, (self.x, self.y))


   









def main():
   pygame.init
   screen = pygame.display.set_mode(SCREENRECT.size)

   # make background
   background = pygame.Surface(SCREENRECT.size).convert()
   background.fill((0,0,255))
   pygame.display.update()

   # keep track of sprites
   all = pygame.sprite.RenderUpdates()

   # keep track of time
   clock = pygame.time.Clock()

   # game loop
   while 1:
      
      # get input
      for event in pygame.event.get():
         if event.type == QUIT: #'or event.key == K_ESCAPE:
            return

         #clear sprites
         all.clear(screen, background)

         # update sprites
         all.update()

         # redraw sprites
         dirty = all.draw(screen)
         pygame.display.update(dirty)

         # maintain frame rate
         clock.tick(30)


if __name__ == '__main__': main()




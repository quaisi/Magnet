#!/bin/usr/env = python

import os
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning fonts disabled'
if not pygame.mixer: print'Warning sound disabled'

#functions to create resources

def load_image(name, colorkey=None):
   fullname = os.path.join('data',name)
   try:
      image = pygame.image.load(fullname)
   except pygame.error, message:
      print 'Cannot load image:', fullname
      raise SystemExit, message
   image = image.convert()
   if colorkey is not None:
      if colorkey is -1:
         colorkey = image.get_at((0,0))
      image.set_colorkey(colorkey, RLEACCEL)
   return image, image.get_rect()

def load_sound(name):
   class NoneSound:
      def play(self): pass
   if not pygame.mixer or not pygame.mixer.get_init():
      return NoneSound()
   fullname = os.path.join('data', name)
   try:
      sound = pygame.mixer.Sound(fullname)
   except pygame.error, message:
      print 'Cannot load sound:', fullname
      raise SystemExit, message
   return sound


# Classes start here

class Hero(pygame.sprite.Sprite):
   """Our main hero follows the mouse"""
   
   def __init__(self):
      self.polarity = True
      pygame.sprite.Sprite.__init__(self) # Sprite initializer
      self.image, self.rect = load_image('fire.png', -1)

   def update(self):
      """move based on mouse position"""
      pos = pygame.mouse.get_pos()
      self.rect.midtop = pos

   def change_polarity(self):
      if self.polarity == True:
         self.polarity = False
      else:
         self.polarity = True

   def get_polarity(self):
      return self.polarity



class Enemy(pygame.sprite.Sprite):
   """Balls of power that want to kill you 
      They are attracted or repelled by polarity
   """
   

   def __init__(self, xpos, ypos, pol, hero):
      self.hero = Hero()
      self.x = xpos
      self.y = ypos
      self.polarity = pol
      pygame.sprite.Sprite.__init__(self)
      
      self.image, self.rect = load_image('fire.png', -1)

   def update(self):
      if self.polarity == True:
         pass
      if self.polarity == False:
         pass

   def set_position(self, xpos, ypos):
      self.x = xpos
      self.y = ypos

"""   def follow_hero():
      x,y = pygame.mouse.get_pos()
      dx = self.hero.x - x
      dy = self.hero.y - y
      self.x = dx / 5
      self.y = dx / 5
"""

def main():
   pygame.init()
   screen = pygame.display.set_mode((800,800))
   pygame.display.set_caption('Magnet')
   pygame.mouse.set_visible(0)

   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((0,0,0))

   if pygame.font:
      font = pygame.font.Font(None, 36)
      text = font.render("This is my test text", 1,(10,10,10))
      textpos = text.get_rect(centerx = background.get_width()/2)
      background.blit(text, textpos)

   screen.blit(background, (0,0))
   pygame.display.flip()

   magnet = Hero()
   ball = Enemy(500,500, True, magnet)

   # Set up enemy lists
   enemies = []
   x = 0
   
   for count in range(10):
      enemies.append(Enemy(50 * x + 50, -200, 'fire.png', magnet))
      x +=10
   #rendering list
   allsprites = pygame.sprite.RenderPlain((magnet, enemies, ball))
   clock = pygame.time.Clock()


   #main loop
   while 1:
      clock.tick(60)
      
      for event in pygame.event.get():
         if event.type == QUIT:
            return
         elif event.type == MOUSEBUTTONDOWN:
            magnet.change_polarity()
      
      allsprites.update()

      #Draw all
      screen.blit(background, (0,0))
      allsprites.draw(screen)
      pygame.display.flip()

if __name__ == '__main__':
   main()

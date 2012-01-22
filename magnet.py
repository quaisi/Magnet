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

class Hero(pygame.sprite.Sprite):
   """Our main hero follows the mouse"""
   
   def __init__(self):
      self.polarity = True
      pygame.sprite.Sprite.__init__(self) # Sprite initializer
      self.image, self.rect = load_image('rocket.png', -1)

   def update(self):
      """move based on mouse position"""
      pos = pygame.mouse.get_pos()
      self.rect.midtop = pos

   def change_polarity(self):
      if self.polarity == True:
         self.polarity = False
      else:
         self.polarity = True
      



def main():
   pygame.init()
   screen = pygame.display.set_mode((500,500))
   pygame.display.set_caption('Magnet')
   pygame.mouse.set_visible(0)

   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((250, 250,250))

   if pygame.font:
      font = pygame.font.Font(None, 36)
      text = font.render("This is my test text", 1,(10,10,10))
      textpos = text.get_rect(centerx = background.get_width()/2)
      background.blit(text, textpos)

   screen.blit(background, (0,0))
   pygame.display.flip()

   magnet = Hero()
   allsprites = pygame.sprite.RenderPlain((magnet))
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

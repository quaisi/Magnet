#!/bin/usr/env = python

import os, random
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


# Classes start here ----------------------------------------


class Hero(pygame.sprite.Sprite):
   """Our main hero follows the mouse"""
   polarity = True
   SCORE = 0

   def __init__(self):
      pygame.sprite.Sprite.__init__(self) # Sprite initializer
      self.image, self.rect = load_image('fire.png', -1)

   def update(self):
      """move based on mouse position"""
      pos = pygame.mouse.get_pos()
      self.rect.midtop = pos

   def change_polarity(self):
      if Hero.polarity == True:
         Hero.polarity = False
      else:
         Hero.polarity = True

class Enemy(pygame.sprite.Sprite):
   """Balls of power
      They are attracted or repelled by polarity
   """
   def __init__(self, xpos, ypos, polarity):
      pygame.sprite.Sprite.__init__(self)
      
      self.x = xpos
      self.y = ypos
      self.polarity = polarity
      self.image, self.rect = load_image('fire.png', -1)
      self.xmoveamount = random.randint(-10,10)
      self.ymoveamount = random.randint(-10,10)
      self.screen = pygame.display.get_surface()

   def set_position(self, xpos, ypos):
       self.x = xpos
       self.y = ypos
   
   def move(self):
      self.rect.midtop = (self.x, self.y)
           
      mousex,mousey = pygame.mouse.get_pos()
      
      dx = self.x - mousex
      dy = self.y - mousey

      if self.polarity == True and Hero.polarity == True:
         self.reverse_direction()

         """self.x = self.x - self.xmoveamount
         self.y = self.y - self.ymoveamount"""
      elif self.polarity == True and Hero.polarity == False:
         self.x -= dx / 10
         self.y -= dy / 10
      elif self.polarity == False and Hero.polarity == True:
         self.x -= dx / 10
         self.y -= dy / 10
      else:
         """self.x = -self.x - self.xmoveamount
         self.y = -self.y - self.ymoveamount"""
         self.reverse_direction()

      self.rect.midtop = (self.x,self.y)
      
   def update(self):
      self.move()
   
   def isOffScreen(self):
      if self.x < 0 or self.y >= MAXX:
         return True
      elif self.y <0 or self.y >= MAXY:
         return True
      return False
   
   def reverse_direction(self):
      self.x = self.x - self.xmoveamount
      self.y = self.y - self.ymoveamount

class Score(pygame.sprite.Sprite):
   def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.font = pygame.font.Font(None, 36)
      #self.font.set_italic(1)
      self.color = Color('white')
      self.lastscore = -1
      self.update()
      self.rect = self.image.get_rect().move(10,450)

   def update(self):
      if Hero.SCORE != self.lastscore:
         self.lastscore = Hero.SCORE
         
         msg = "Score: %d" % int(Hero.SCORE)
         self.image = self.font.render(msg, 0, self.color)

      
      """
   if pygame.font:
      font = pygame.font.Font(None, 36)
      text = font.render("Score", 1,(255,255,255))
      textpos = text.get_rect(centerx = background.get_width()/2)
      background.blit(text, textpos)"""

# Main function ---------------------------------------------------   

def main():
   scores = [] 
   polarity = True
   pygame.init()
   MAXX = 800
   MAXY = 800
   
   screen = pygame.display.set_mode((MAXX, MAXY))
   pygame.display.set_caption('Magnet')
   pygame.mouse.set_visible(0)

   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((0,0,0))

   screen.blit(background, (0,0))
   pygame.display.flip()

   magnet = Hero()
   score = Score()

   #rendering list
   allgroup = pygame.sprite.Group()
   enemygroup = pygame.sprite.Group()
   
   scoregroup = pygame.sprite.RenderPlain(score)

   herogroup = pygame.sprite.Group()
   herogroup = pygame.sprite.RenderPlain((magnet))


   clock = pygame.time.Clock()
   
   
   #counter to generate new enemy every counter times through main loop
   counter = 0
   
   # Get an enemy on when starting
   enemygroup.add(Enemy(random.randint(0,MAXX), \
         random.randint(0,MAXY), True))
   
   
   #main loop---------------------------------------------------------
   while 1:
      Hero.SCORE += 1
      clock.tick(60)
            
      for event in pygame.event.get():
         if event.type == QUIT:
            return
         elif event.type == MOUSEBUTTONDOWN:
            if Hero.polarity == True:
               Hero.polarity = False
            else:
               Hero.polarity = True
      enemygroup.update()
      herogroup.update()
      scoregroup.update()

      # Check for collisions
      if pygame.sprite.spritecollide(magnet, enemygroup, True):
         print "Collision - Score: %d" % int(Hero.SCORE)
         scores.append(Hero.SCORE)
         Hero.SCORE = 0
      
      #Draw all
      screen.blit(background, (0,0))
      herogroup.draw(screen)
      enemygroup.draw(screen)
      scoregroup.draw(screen)
      pygame.display.flip()

      if counter >=50:
         counter = 0
         enemygroup.add(Enemy(random.randint(0,MAXX),
            random.randint(0,MAXY), random.choice([True, False])))
      counter = counter + 1
if __name__ == '__main__':
   main()

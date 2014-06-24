##@file

##@namespace xmovie
#This module has responsibilty for all movie playing

#!/usr/bin/env python

import os, sys

import pygame
from pygame.locals import *

from xutils import movie_load

## Class XMovie
# Encapsluates the playing of a movie in the iDore system
class XMovie(pygame.sprite.Sprite):
	
	## XMovie Constructor<br>
	# @param self The object pointer
	# @param element The XElement that describes this moview
    def __init__(self, element):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

        self.movie = movie_load(element.get_attr_string('src'))
        x = element.get_attr_int('x')
        y = element.get_attr_int('y')
        width = element.get_attr_int('width')
        height = element.get_attr_int('height')
        self.rect = Rect(x, y, width, height)
        self.image = pygame.Surface(self.rect.size)
        self.movie.set_display(self.image, (0,0)+self.rect.size)
        self.movie.set_volume(1)
        
        self.finished_handler = None
    
    def __del__(self):
        self.movie.stop()
        del(self.movie)
	
	## Play movie<br>
	# This plays the current XMovie
	# @param self The object pointer
    def play(self):
        self.movie.play()
        print "Audio", self.movie.has_audio(), "Video", self.movie.has_video()
    
	## Stop movie<br>
	# This stops the current XMovie
	# @param self The object pointer 
    def stop(self):
        self.movie.stop()
    
	## Set Movie finished Handler<br>
	# Sets the function that will be called when the movie has finished
	# @param self The object pointer
	# @param handler The function which handles movie finished events 
    def set_finished_handler(self, handler):
        self.finished_handler = handler
        
#--------------------------------------------------------------------

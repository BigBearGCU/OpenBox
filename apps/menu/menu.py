#!/usr/bin/env python

import os, sys

import pygame
from pygame.locals import *

from common.framework.xglobals import *
from common.framework.xframework import *
from common.framework.xxml import xml_load
from common.framework.xgame import XGame
from common.framework.xbutton import *

class Menu(XGame):
	
	def __init__(self,element):
		XGame.__init__(self,element)
		self.exit = False
		self.show_screen("main")
		self.exitButton=self.get_object("backButton")
		self.exitButton.set_handler(self.buttonHandler)
		self.startButton=self.get_object("forwardButton")
		self.startButton.set_handler(self.buttonHandler)
		

	def __del__(self):
		XGame.__del__(self)
	
	def buttonHandler(self, btn, state):
		if state != xbuttonFired:
			return
		
		if btn==self.exitButton:
			self.exit=True
		if btn==self.startButton:
			self.exit=True
			
	def main_loop(self):
		
		clock = pygame.time.Clock()
		physicsTime = 1000.0/gFps
		
		while not self.exit:
			elapsedTime = clock.tick(gFps)
			self.update_world(physicsTime)
			self.update_display(clock)
			for event in pygame.event.get():
				if (self.check_event(event)):
					return
		return -1

def run():

	game = Menu('menu.xml')
	ret = game.start()
	game.start()
	game.stop()
	del game
	return ret
	
if __name__ == '__main__':

	# Import Psyco if available
	try:
		
		import psyco
		psyco.log()
		psyco.full(memory=100)
		psyco.profile(0.05, memory=100)
		psyco.profile(0.2)
	except ImportError:
		pass

	run()
	del_framework()

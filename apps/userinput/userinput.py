#!/usr/bin/env python

import os, sys

import pygame
from pygame.locals import *

from common.framework.xglobals import *
from common.framework.xframework import *
from common.framework.xxml import xml_load
from common.framework.xgame import XGame

class UserInputTest(XGame):
	
	def __init__(self,element):
		XGame.__init__(self,element)
		self.exit = False
		self.show_screen("test")
		self.card=self.get_object("testcard")
		

	def __del__(self):
		XGame.__del__(self)
		
	def main_loop(self):
		
		clock = pygame.time.Clock()
		physicsTime = 1000.0/gFps
		
		while not self.exit:
			elapsedTime = clock.tick(gFps)
			self.update_world(physicsTime)
			self.update_display(clock)
			
			if (self.isKeyPressed(K_RIGHT)):
				self.card.move((1,0))
			elif (self.isKeyPressed(K_LEFT)):
				self.card.move((-1,0))
			if (self.isKeyPressed(K_UP)):
				self.card.move((0,-1))
			elif (self.isKeyPressed(K_DOWN)):
				self.card.move((0,1))
			
			if (self.isMouseButtonPressed(0)):
				pos=self.getMouseCursorPos()
				self.card.set_pos(pos)
			
			#joystick=self.getJoystickState(0)
			#axis0=joystick.get_axis(0)*10
			#axis1=joystick.get_axis(1)*10
			#print "Axis "+str(axis0)+" Axis "+str(axis1)
			#self.card.move((axis0,axis1))
			
			for event in pygame.event.get():
				if (self.check_event(event)):
					return
		return -1

def run():
	game = UserInputTest('userinput.xml')
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

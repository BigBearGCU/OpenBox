

import pygame
from pygame.locals import *


class XJoystick:
	def __init__(self,joystick):
		self.scale=2
		self.threshold=0.6
		self.joystick=joystick
	
	def init(self):
		self.joystick.init()
	
	def get_axis(self,axis):
		value=self.joystick.get_axis(axis)
		if (value<0.0):
			if (value>self.threshold):
				value=0.0
		elif (value>0.0):
			if (value<self.threshold):
				value=0.0
		
		return value*self.scale
	
	def get_button(self,button):
		return self.joystick.get_button(button)

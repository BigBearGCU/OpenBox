import os, sys

import pygame
from pygame.locals import *

from xutils import *
from xsprite import XSprite

class XMouseCursor(XSprite):
	 
	 def __init__(self,element=None):
		 XSprite.__init__(self,element)
		 

##@file

##@namespace xscreenshot
#constains classes to deal with a screenshot system for
#the idore project
import os, sys
import pygame
from pygame.locals import *

from common.framework.xframework import *
from common.framework.xgame import *
##Class XScreenShot
class XScreenShot:
	
	def __init__(self,savePath,filename):
		self.count=0
		framework=get_framework()
		self.path=os.path.join(framework.gcalpath,savePath)
		if os.path.exists(self.path):
			pass
			#count how many in here
			#set index to count -1
		else:
			os.mkdir(self.path)
			self.count=0
		self.filename=filename
		self.image=None
		self.file=open(os.path.join(self.path,self.filename+".txt"),"w")
	
	def save(self,gameSurface):
		self.image=gameSurface
		if os.path.exists(self.path):
			finalFilename=os.path.join(self.path,self.filename+str(self.count)+".tga")
			print finalFilename
			pygame.image.save(self.image,finalFilename)
			self.file.write(self.filename+str(self.count)+".tga\n")
			self.count=self.count+1
			#pygame.image.save(self.displaySurface,os.path.join(self.framework.savepath,"screendump.tga"))
	
	def saveToFile(self,gameSurface,filename):
		self.filename=filename
		self.save(gameSurface)
		
	def getScreenshort(self):
		return self.image
	
	def __del__(self):
		self.file.close()



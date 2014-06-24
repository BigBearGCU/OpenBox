import os
from lib.common.framework.xxml import *

class Game:
	def __init__(self,element=None):
		if element:
			self.id=element.get_attr_string("id")
			self.title=element.get_attr_string("title")
			self.imp=element.get_attr_string("imp")
			self.cwd=element.get_attr_string("cwd")
			self.app=element.get_attr_string("app")
			self.desc=element.get_attr_string("desc")
			

class GameList:
	def __init__(self,filename):
		self.gameDict={}
		if os.path.exists(filename):
			element=xml_load(filename)
			element.debug()
			self.populate(element)
	
	def populate(self,element):
		for e in element.elements:
			game=Game(e)
			self.add(game.id,game)
	
	def add(self,id,game):
		self.gameDict[id]=game
	
	def getGame(self,id):
		return self.gameDict[id]
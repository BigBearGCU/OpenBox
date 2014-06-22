#!/usr/bin/env python

## @file

## @namespace xgame
# All genric game code will be contained in this module

import os, sys,platform

import pygame
from pygame.locals import *

from xglobals import *
from xframework import *
from xwebcam import XWebcam
from xmovie import XMovie
from xbutton import *
from xsprite import XSprite
from ximage import XImage
from xphysics import XPhysics
from xmousecursor import XMouseCursor
from xutils import image_load, movie_load
from xxml import xml_load
from xtext import XFontManager, XText
from xscreenshot import XScreenShot
from xjoystick import XJoystick

## Clear a Specfied rectangle to red<br>
# @param surf The draw surface we are clearing
# @param rect The rectangle we are clearing on the surface
def clear_callback(surf, rect):
	color = (255, 0, 0)
	surf.fill(color, rect)

## XGame class<br>
# The base class for all games in the iDore system, this class 
# deals with the loading of a game from Xml, game updates and
# drawing game elements to the screen
class XGame:
	
	## XGame constructor<br>
	# Loads the game from xml and initalises all game
	# subsystems
	# @param self The object pointer
	# @param xmlFilename The name of the XML filename that
	# holds the various elements in the game
	def __init__(self,xmlFileName):
		#joystick list, 
		self.joysticks={}
		self.mouseCursor=None
		self.mouseButton=()
		element = xml_load(xmlFileName)
		self.initialise(element)
		
	## Initailses all Game subsytems and all other game elements<br>
	# This function initialises all game subsystems, sets up all sprite groups
	# @param self The object pointer
	# @param element The XElement that describes our game
	def initialise(self, element=None):
		self.takeMovie=False
		self.framework = get_framework()
		self.fontManager = self.framework.get_font_manager()
		self.font = self.fontManager.get_font()
		
		self.bgImage = None

		self.imageGroup = pygame.sprite.Group()  ## For update
		self.spriteGroup = pygame.sprite.Group() ## For collision detection
		self.buttonGroup = pygame.sprite.Group() ## For collision detection

		self.updateRect = False  ## Update whole screen or just dirty rects
		self.layers = []

		self.screen = None
		self.videoList = []      ## The movie and webcam objects
		self.movie = None
		self.oldMovie = None
		self.movieActive = False

		self.physics = XPhysics()

		self.webcam = None
		self.webcamTime = 0
		self.doCollision = False
		self.newBlobs = False
		self.blobSprites = []
		self.displaySurface=None
		self.keys=[]
		
		for i in range (0,pygame.joystick.get_count()-1):
			pyJoy=pygame.joystick.Joystick(i)
			joystick=XJoystick(pyJoy)
			joystick.init()
			self.framework.log_message("Joystick "+str(pyJoy.get_id()))
			self.framework.log_message("==============")
			self.framework.log_message("Joystick Axis "+str(pyJoy.get_numaxes()))
			self.framework.log_message("Joystick Buttons "+str(pyJoy.get_numbuttons()))
			self.framework.log_message("Joystick Hats "+str(pyJoy.get_numhats()))
			self.framework.log_message("Joystick Balls "+str(pyJoy.get_numballs()))
			self.framework.log_message("")
			self.joysticks[pyJoy.get_id()]=joystick
		
		#self.screenShotSystem=XScreenShot()
		## ToDo: Instationation without an element
		if element:
			self.set_element(element)
						
	def __del__(self):
		if self.movie:
			del self.movie

	## Retrieves all game elements from the XElement passed in<br>
	# This function retrieves all the game elements and options from
	# the XElement object
	def set_element(self, element):
		self.element = element
		
		self.displaySurface = self.framework.get_display_surface() ## May be None
		if self.displaySurface == None:
			size = (self.element.get_attr_int('width'), self.element.get_attr_int('height'))
			flags=0
			if gFullScreen: flags = FULLSCREEN
			self.displaySurface = self.framework.set_display_surface(size, flags)

			#print pygame.display.Info()
			#modes = pygame.display.list_modes(0, pygame.FULLSCREEN)
			#for m in modes: print m
		
		pygame.display.set_caption("OpenBox")
		title=self.element.get_attr_string('id',"None")
		#create screen shot system after display surface has been created
		self.screenShotSystem=XScreenShot("screenshot",title)
		## Show splash screen as soon as possible
		splashFilename = self.element.get_attr_string('splash')
		if splashFilename:
			splash, rect = image_load(splashFilename, None)
			splash = splash.convert()
			self.bgImage = pygame.transform.scale(splash, self.displaySurface.get_size())
			self.displaySurface.blit(self.bgImage, (0,0))
			pygame.display.update()
		
		# Get the wecam
		self.webcam = self.framework.get_webcam()
		
		# build screen dictionary
		self.screenDict = {}
		for e in self.element.elements:
			if e.type == "cursor":
				filename=e.get_attr_string('src')
				if filename:
					filename=os.path.join(self.framework.assetpath,filename)
					sizeX=e.get_attr_int('sizeX',64)
					sizeY=e.get_attr_int('sizeY',64)
					self.mouseCursor=XMouseCursor()
					image, rect = image_load(filename)
					self.mouseCursor.set_image(image, 1, (sizeX, sizeY))
					self.mouseCursor.set_pos((0,0))
			if e.type == "screen":
				try:
					self.screenDict[e.attrs['id']] = e
				except:
					self.screenDict[len(self.screenDict)] = e

	## Starts game<br>
	# This function starts the game by calling the game loop
	# @param self The object pointer
	def start(self):
		return self.main_loop()
	
	def check_event(self,event):
		if event.type == QUIT:
			#add code to convert video
			return True
		elif event.type == KEYUP:
			if event.key==K_ESCAPE:
				#add code to convert video
				return True
			if event.key==K_F4:
				log_message(str(event.key))
				if self.takeMovie==False:
					print "Screenshot"
					self.screenShotSystem.save(self.displaySurface)
			if event.key==K_F12:
				self.takeMovie=not self.takeMovie
		return False
	
	
	## Stops the current movie<br>
	# This function will stop any movie that has played during the course of
	# game
	# @param self The object pointer
	def stop(self):
		if self.movie:
			self.movie.stop()
	
	def object_factory(self, type, element):
		return None
	
	## Shows the specfied screen<br>
	# Sets up the screen as per a <screen> tag in the XML file
	# Objects are layered back to front as they appear in the XML file
	# Although the movie and webcam will always appear beneath other objects
	# @param self The object pointer
	# @param id The id of screen we want to show
	def show_screen(self, id):

		try:
			self.screen = self.screenDict[id]
		except:
			raise NameError("show_screen: screen")

		update = self.screen.get_attr_string('update')
		if update == 'rect':
			self.updateRect = True
		else:
			self.updateRect = False

		self.layers = []
		self.layers.append(pygame.sprite.RenderUpdates())  ## Video / webcam
		self.layers.append(pygame.sprite.OrderedUpdates()) ## Sprites and images
		self.layers.append(pygame.sprite.RenderUpdates())  ## Buttons
		
		bg = self.screen.get_attr_string('bgimage')
		if bg:
			image, rect = image_load(bg, None)
			image = image.convert()
			self.bgImage = pygame.transform.scale(image, self.displaySurface.get_size())

			if self.updateRect:
				self.displaySurface.blit(self.bgImage, (0,0))
				pygame.display.update()                
		else:
			self.bgImage = None

		if self.movie:
			self.movie.stop()
			self.movieActive = False

			# Workaround to prevent movie playback from becoming f*cked
			# even when movie is stopped.
			# The movie is running in a background thread but if the
			# reference to it is lost the garbage collector will jump
			# in and attempt to delete it.            
			self.oldMovie = self.movie
			self.movie = None

		# Create objects from element
		# Allocate them to layers and lists
		# Build object dictionary
		self.videoList = []        
		self.objectDict = {}
		self.imageGroup = pygame.sprite.Group()
		self.spriteGroup = pygame.sprite.Group()
		self.buttonGroup = pygame.sprite.Group()
		
		hadWebcam = False
		
		for e in self.screen.elements:
			if e.type == "image":
				self.add_object(XImage(e))
			elif e.type == "sprite":
				self.add_object(XSprite(e))
			elif e.type == "button":
				self.add_object(XButton(e))
			elif e.type == "font":
				self.fontManager.create_font_from_element(e)
			elif e.type == "text":
				self.add_object(XText(self.fontManager, e))
			elif e.type == "movie":
				assert not self.movieActive # only one per screen
				self.movieActive = True
				pygame.mixer.quit()
				self.movie = XMovie(e)
				self.videoList.append(self.movie)
				self.layers[0].add(self.movie)
			elif e.type == "webcam":
				assert not hadWebcam # only one per screen
				hadWebcam = True
				self.webcam.set_element(e)
				self.videoList.append(self.webcam)
				self.layers[0].add(self.webcam)
			else:
				# Give subclass a change to instantiate the object
				o = self.object_factory(e.type, e)
				if o: self.add_object(o)
		
		# Movie setup
		if self.movieActive:
			self.movie.play()
		else:
			# The pygame mixer and movie objects are shit.
			# If we have played a movie it will take a time for that thread to die
			# and release whatever the mixer needs to initialise.
			# Try this in a loop a few times.
			count = 0  
			while pygame.mixer.get_init() == None and count < 5:
				print "Trying to init mixer..."
				pygame.mixer.quit()
				pygame.time.wait(1000)
				pygame.mixer.init()
				count += 1

		# Webcam setup  
		if hadWebcam:
			self.webcam.start()
		elif self.webcam.is_active():
			self.webcam.stop()

		## Reset motion detection
		self.doCollision = False
		self.newBlobs = False
		self.blobSprites = []
	
	def getKeyState(self):
		pygame.event.pump()
		return pygame.key.get_pressed()
	
	def getMouseButtonState(self):
		pygame.event.pump()
		return pygame.mouse.get_pressed()
	
	def isMouseButtonPressed(self,mouseButton):
		self.mouseButton=self.getMouseButtonState()
		return self.mouseButton[mouseButton]
	
	def isKeyPressed(self,key):
		self.keys=self.getKeyState()
		return self.keys[key]
	
	def getMousePosition(self,rel):
		pygame.event.pump()
		if (rel):
			return pygame.mouse.get_rel()
		else:
			return pygame.mouse.get_pos()
	
	def getMouseCursorPos(self):
		if (self.mouseCursor):
			return self.mouseCursor.get_pos()
		else:
			return self.getMousePosition(True)
	
	def getJoystickState(self,id):
		pygame.event.pump()
		return self.joysticks[id]
	
	## Retrieve an object from the game<br>
	# Allow parent object access to buttons, sprites, images defined in XML
	# For efficiency caller should really get these references
	# once and store them rather than keep calling this function.
	# @param self The object pointer
	# @param id The id of the object

	def get_object(self, id):
		try:
			return self.objectDict[id]
		except:
			#print "XGame.get_object: failed", id
			return None

	## Add object<br> 
	# Adds an object such as XSprite, XImage, XText or XButton
	# to the screen
	# @param self The object pointer
	# @param object The object to add to the screen
	# @param dict Add this object to the object dictonary 
	def add_object(self, object, dict=True):
		isText = issubclass(type(object), XText)
		isSprite = issubclass(type(object), XSprite)
		isImage = issubclass(type(object), XImage)
		isButton = issubclass(type(object), XButton)
		if isSprite:
			self.framework.log_message("Is Sprite "+str(object))
			self.spriteGroup.add(object)
			self.layers[1].add(object)
		elif isImage or isText:
			self.framework.log_message("Is Image "+str(object))
			self.imageGroup.add(object)
			self.layers[1].add(object)
		elif isButton: 
			self.framework.log_message("Is Button "+str(object))
			self.buttonGroup.add(object)
			self.layers[2].add(object)	
		if dict:
			try:
				self.objectDict[object.id] = object
			except:
				self.objectDict[len(self.objectDict)] = object
	
	## Remove object<br>
	# Removes an object such as XSprite, XImage, XText or XButton
	# from the screen
	# @param self The object pointer
	# @param object The object to remove from the screen
	# @param dict Remove this object from the object dictonary 
	def remove_object(self, object, dict=True):
		isText = issubclass(type(object), XText)
		isSprite = issubclass(type(object), XSprite)
		isImage = issubclass(type(object), XImage)
		isButton = issubclass(type(object), XButton)
		if isSprite: 
			self.spriteGroup.remove(object)
			self.layers[1].remove(object)
		elif isImage or isText:
			self.imageGroup.remove(object)
			self.layers[1].remove(object)
		elif isButton: 
			self.buttonGroup.remove(object)
			self.layers[2].remove(object)
		try:
			self.objectDict[object.id].remove
		except:
			print "XGame.remove_object: failed to remove object from dictionary", object

	def show_object(self, object):        
		self.add_object(object, False)
		object.visable = True
		
	def hide_object(self, object):
		object.visable = False
		self.remove_object(object, False)

	def hide_webcam(self):
		self.webcam.set_blank(True)

	## Get webcam mask<br>
	# For querying the colour value at a given point of the webcam mask.
	# Returns (r, g, b) or none if no mask set.
	# @param self The object pointer
	# @param pos The screen position to check
	# @returns The r,g,b colours of the mask at that position
	def get_webcam_mask_val(self, pos):
		if self.webcam.is_active():
			return self.webcam.get_mask_val(pos)
		else:
			return None
		
	## Update game
	# Updates the game. Checks webcam for user interaction, check collision
	# detection between sprites and updates the state of all attached objects
	# @param self The object pointer
	# @param elapsedTime The elapsed time since the last game update 
	def update_world(self, elapsedTime):
	
		if self.webcam.is_active():
			
			self.webcamTime -= elapsedTime
			if self.webcamTime < 0:
				## Spread load by getting image one frame and motion detection the next
				if not self.doCollision and self.webcam.get_image():
					self.doCollision = True
				elif self.doCollision:
					self.blobSprites = self.webcam.detect_motion(elapsedTime, self.displaySurface.get_size())
					self.doCollision = False
					self.newBlobs = True
					self.webcamTime = 1000 / gWebcamFps
		
		if self.movieActive and not self.movie.movie.get_busy():
			self.movieActive = False
			if self.movie.finished_handler:
				self.movie.finished_handler()

		self.physics.update_world(elapsedTime, self.buttonGroup, self.spriteGroup, self.blobSprites)
		
		if (self.mouseCursor):
			mousePos=self.getMousePosition(True)
			self.mouseCursor.move(mousePos)
			if (self.isMouseButtonPressed(0)):
				buttons=pygame.sprite.spritecollide(self.mouseCursor, self.buttonGroup, False)
				for b in buttons:
					b.set_state(xbuttonFire)
		
		for o in self.imageGroup, self.spriteGroup, self.buttonGroup:
			o.update(elapsedTime)
		if (self.mouseCursor):
                        self.mouseCursor.update(elapsedTime)
							
	## Get the drawing surface of this game<br>
	# Retrieves the surface that we are drawing on in the game
	# @param self The object pointer
	# @returns displaySurface The drawing surface
	def get_display_surface(self):
		return self.displaySurface
							
	## Updates the drawing surface<br>
	# Draws all objects to the screen
	# @param self The object pointer
	# @param clock Displays the Frame Per Second to the screen
	def update_display(self, clock=None):
	
		if self.updateRect:
			
			if self.bgImage:
				for layer in self.layers:
					layer.clear(self.displaySurface, self.bgImage)
				
			# the rect's of the layers are added to the rectlist
			# with display.update only nedded parts of the display are redrawn
			self.rectlist = []
			for layer in self.layers:
				self.rectlist.extend(layer.draw(self.displaySurface))
			
			if clock:
				if gShowFPS:
					actualFps = int(clock.get_fps())
					text = self.font.render(repr(actualFps), True, (255, 0, 0), (255, 255, 255))
					self.displaySurface.blit(text, (10, 10))
					self.rectlist.append(Rect((10, 10), text.get_size()))
			#we could have added this to a group but we are just going to render this
			#outside the group
			if self.mouseCursor:
					self.displaySurface.blit(self.mouseCursor.theImage,self.mouseCursor.get_pos())
					self.rectlist.append(self.mouseCursor.rect)
					
			pygame.display.update(self.rectlist)
				
		else:

			if self.bgImage:
				self.displaySurface.blit(self.bgImage, (0,0))
				
			for layer in self.layers:
				layer.draw(self.displaySurface)
			

			if clock:
				if gShowFPS:
					actualFps = int(clock.get_fps())
					text = self.font.render(repr(actualFps), True, (255, 0, 0), (255, 255, 255))
					self.displaySurface.blit(text, (10, 10))
			
			#we could have added this to a group but we are just going to render this
			#outside the group
			if self.mouseCursor:
				self.displaySurface.blit(self.mouseCursor.theImage,self.mouseCursor.get_pos())
			
			pygame.display.update()
		if self.takeMovie:
			self.screenShotSystem.save(self.displaySurface)

#--------------------------------------------------------------------

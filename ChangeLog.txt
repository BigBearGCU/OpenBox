
Application Template Change Log and ToDo List
=============================================

Source 8
--------
04/05/2007 Now take a buffer from VideoCapture library rather than taking 
           a PIL image and converting it to a Pygame image.  
           However no great performance improvements gained.
04/05/2007 Renamed class Actor to XSprite and made into library.
04/05/2007 Motion detection now passed up to XSprite and XButton.

Source 9
--------
07/05/2007 Can now play MPEG audio/video movies in a video window using
           XMovie created via the <movie> tag.

Source 10
---------
09/05/2007 Implemented XWebcam class.  Can now place webcam anywhere on
           screen with a choice of resolutions using the <webcam> tag.

Source 11
---------
09/05/2007 Implemented XImage class which will display an image strip as
           as an animation.  Can now place images anywhere on screen using
           the <image> tag.           
09/05/2007 XSprite can now animate image strips just as XImage can.

Source 12
---------
09/05/2007 Added loop attribute to <sprite> and <image>
10/05/2007 Hooked up motion detection into new object heirarchy.
           Motion detection now able to cope with change of resolution
           between screens.

Source 13
---------
10/05/2007 XButton now has three sub-images that are animated in time with
           state changes and triggered by motion from the webcam.

Source 14
---------
16/05/2007 Now do conditional execution depending upon system (Linux or
           Windows) so that webcam works on both systems.
17/05/2007 Scale splash and bgimage to screen size (although art should be
           produced to fit or at least correct aspect ratio).
17/05/2007 Moved main loop from xgame.py into game.py.
17/05/2007 Made game full screen.

Source 15
---------
17/05/2007 Added physics engine and collision detection.
           Bug when objects collide they sometimes stick together.
           Probably overlapping each other.

Source 16
---------
19/05/2007 Fixed objects sticking together during collision detection.

Source 17
---------
21/05/2007 XSprite and XImage optimised update() function calling.
22/05/2007 If a screen does not define bgimage then it will no longer
           inherit previous screens.  Allows for faster update on full screen
           webcams/movies.
22/05/2007 Moved webcam capturing into seperate thread to improve performance.

Source 19
---------
25/05/2007 Use psycho in game.py
25/05/2007 Add call to wait in webcam thread to give time back to main thread.
26/05/2007 Can now define update type per screen in xml (rect or all)
26/05/2007 Can now set webcam fps to improve performance

Source 20
---------
26/05/2005 Added a mask facility to the webcam to mask out regions.
           Speeded up the webcam stuff even more as realised don't need to copy
           the image as convert() does that already.

Source 21
---------
29/05/2005 Changed layering. Sprites and images on own ordered layer, buttons
           on top layer.

Source 22
---------
31/05/2007 Implemented webcam interaction with sprites using XBlobs which
           act like invisible sprites.  Still needs tidying up though.

Source 23
---------
31/05/2007 Optimised flood fill when building blobs.
31/05/2007 Optimised rectangles for collision testing of blobs.

Source 24
---------
03/06/2007 Fixed bug where webcam thread was not stopping on exit.
03/06/2007 XBlobSprite now persist across frames for motion detection.
03/06/2007 Hooked up XButton to new XBlobSprite motion detection.
03/06/2007 Now determine previous related blob by proximity.

Source 25
---------
05/06/2007 Implemented copy of XImage, XSprite and XButton and ability to
           add them to the drawing layers.

Source 26
---------
07/06/2007 Masking - now a cell is masked if its red channel is 0.
07/06/2007 XGame - auto determine if objects need adding to sprite/button groups.
07/06/2007 XPhysics - protect from division by zero.
08/06/2007 Implemented example game "trail" and fixed related issues.

Source 27
---------
08/06/2007 XWebcam now handles PC, video4linux and video4linux2 (although tis not nice).
10/06/2007 XGame now sets a flag self.newBlobs to True after motion detection has been
           performed.

Source 28
---------
14/06/2007 Can now query colour value at a point int the webcam mask.
14/06/2007 Can now set time it takes image to cycle through its frames using
           duration attribute (in millisenconds).
14/06/2007 Implemented XPhysics.do_blob_collision_test_with_delay which only allows a blob
           to colide with a sprite once every half a second.  This is to help prevent 
           wierd collisions cuased when blob passes through sprite.

Source 29
---------
15/06/2007 Fixed problem with mask (was using top left pixel as alpha colour).
15/06/2007 Correctly stopping video capture on Linux - however still unreliable!
15/06/2007 Can now define motion detection algorithm in XML by setting webcam 
           detect attribute ("motion" or "change").

ToDo:
-----
Particle system
Hint text
Clean handling of common errors (no webcam, missing media, etc)
Text on buttons or screen with fonts, colours, anti-aliasing, etc
Saving webcam image files
Integration with pyODE
Video player controls and events when finished
Blob velocity damping

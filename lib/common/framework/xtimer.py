class Timer:

	def __init__(self, delayMillisec, callback):
		self.delayMillisec = delayMillisec
		self.callback = callback
		self.time = 0
		self.fired = False

	def update(self, elapsedMillisec):
		if not self.fired:
			self.time += elapsedMillisec
			if self.time >= self.delayMillisec:
				self.fired = True
				self.callback(self)
	
	def reset(self):
		self.time = 0        
		self.fired = False

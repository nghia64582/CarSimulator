from Draw import *

class ReferSystem:
	def __init__(self,p,zoom):
		self.p = p
		self.zoom = zoom
	def centralize(self,point):
		self.p.x = screenWidth  / 2 - point.x*self.zoom
		self.p.y = screenHeight / 2 - point.y*self.zoom
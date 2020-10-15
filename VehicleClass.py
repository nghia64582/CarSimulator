from math import *
from StateClass import *
from PointClass import *
from Draw import *
import numpy as np

class Vehicle:
	#  1-2-3
	#  |   |
	#  | 7 |
	#  |   |
	#  4-5-6
	# central of state is point 7
	def __init__(self,state,speed,color):
		self.state = state
		self.speed = speed
		self.color = color
		self.length = 2.4
		self.width = 1.6
		self.wheelbase = 2.7

	def isCollision(self,obstacleList):
		for obstacle in obstacleList:
			if self.state.isCollision(obstacle):
				return True
		return False

	def nextPosition(self,t):
		# calculate state of car in next t seconds
		# case 1: alpha2 = 0
		# case 2: alpha2 >< 0
		# step 1: find center of turning circle
		# step 2: find perimeter then calculate how much distance did the car move?
		# step 3: set new state
		# demo by demo.png and demo1.png (in folder)

		newState = State(Point(0,0),0,0)
		# case 1: self.state.alpha2 ~ 0
		if self.state.alpha2 % 360 < 1e-2:
			newState.alpha1 = self.state.alpha1
			newState.alpha2 = self.state.alpha2
			movedDistance = self.speed * t
			newState.central.x = self.state.central.x + movedDistance*cos(newState.alpha1/180*pi)
			newState.central.y = self.state.central.y + movedDistance*sin(newState.alpha1/180*pi)
			return newState

		# step 1
		# point L in image
		p7 = self.state.central
		p5 = Point(0,0)
		p5.x = p7.x-cos(self.state.alpha1/180*pi)*self.length/2
		p5.y = p7.y-sin(self.state.alpha1/180*pi)*self.length/2
		# angle LOI
		alpha3 = 90 - self.state.alpha2
		# angle ILx
		alpha4 = 90 + self.state.alpha1
		IL = self.length*tan(alpha3/180*pi)
		I = Point(0,0)
		I.x = p5.x + IL*cos(alpha4/180*pi)
		I.y = p5.y + IL*sin(alpha4/180*pi)

		# step 2
		radius = IL
		perimeter = radius*2*pi
		movedDistance = self.speed * t

		# step 3
		alpha5 = - (180 - alpha4)
		alpha6 = movedDistance/perimeter*360
		alpha7 = alpha5 + alpha6
		newp5 = Point(0,0)
		newp5.x = I.x + radius*cos(alpha7/180*pi)
		newp5.y = I.y + radius*sin(alpha7/180*pi)
		newState.alpha1 = self.state.alpha1 + alpha6
		newState.alpha2 = self.state.alpha2
		newState.central.x = newp5.x + cos(newState.alpha1/180*pi)*self.length/2
		newState.central.y = newp5.y + sin(newState.alpha1/180*pi)*self.length/2
		return newState

	def move(self,t):
		self.state = self.nextPosition(t)

	def polygonShape(self):
		#  1-2-3
		#  |   |
		#  | 7 |
		#  |   |
		#  4-5-6
		# return 4 corners of the car (1,3,6,4) 
		p7 = self.state.central
		p2 = Point(0,0)
		p2.x = p7.x+cos(self.state.alpha1/180*pi)*self.length/2
		p2.y = p7.y+sin(self.state.alpha1/180*pi)*self.length/2
		p5 = Point(0,0)
		p5.x = p7.x-cos(self.state.alpha1/180*pi)*self.length/2
		p5.y = p7.y-sin(self.state.alpha1/180*pi)*self.length/2
		p1 = Point(0,0)
		p1.x = p2.x+cos((self.state.alpha1+90)/180*pi)*self.width/2
		p1.y = p2.y+sin((self.state.alpha1+90)/180*pi)*self.width/2
		p3 = Point(0,0)
		p3.x = p2.x+cos((self.state.alpha1-90)/180*pi)*self.width/2
		p3.y = p2.y+sin((self.state.alpha1-90)/180*pi)*self.width/2
		p4 = Point(0,0)
		p4.x = p5.x+cos((self.state.alpha1+90)/180*pi)*self.width/2
		p4.y = p5.y+sin((self.state.alpha1+90)/180*pi)*self.width/2
		p6 = Point(0,0)
		p6.x = p5.x+cos((self.state.alpha1-90)/180*pi)*self.width/2
		p6.y = p5.y+sin((self.state.alpha1-90)/180*pi)*self.width/2
		return Polygon([p1,p3,p6,p5,p7,p5,p4])
		# return Polygon([p1,p3,p6,p4])

	def pointList(self,listId):
		# return Polygon with listId
		pointList = []

		return Polygon([point for point in pointList])

	def pointInVehicle(self,idx):
		#  1-2-3
		#  |   |
		#  | 7 |
		#  |   |
		#  4-5-6
		p = Point(0,0)
		if idx == 1:
			p.x = self.state.central.x + self.length / 2 * cos(self.state.alpha1/180*pi) + self.width / 2 * cos((self.state.alpha1+90)/180*pi)
			p.y = self.state.central.y + self.length / 2 * sin(self.state.alpha1/180*pi) + self.width / 2 * sin((self.state.alpha1+90)/180*pi)
		if idx == 2:
			p.x = self.state.central.x + self.length / 2 * cos(self.state.alpha1/180*pi)
			p.y = self.state.central.y + self.length / 2 * sin(self.state.alpha1/180*pi)
		if idx == 3:
			p.x = self.state.central.x + self.length / 2 * cos(self.state.alpha1/180*pi) + self.width / 2 * cos((self.state.alpha1-90)/180*pi)
			p.y = self.state.central.y + self.length / 2 * sin(self.state.alpha1/180*pi) + self.width / 2 * sin((self.state.alpha1-90)/180*pi)
		if idx == 4:
			p.x = self.state.central.x + self.length / 2 * cos((self.state.alpha1-180)/180*pi) + self.width / 2 * cos((self.state.alpha1+90)/180*pi)
			p.y = self.state.central.y + self.length / 2 * sin((self.state.alpha1-180)/180*pi) + self.width / 2 * sin((self.state.alpha1+90)/180*pi)
		if idx == 5:
			p.x = self.state.central.x + self.length / 2 * cos((self.state.alpha1-180)/180*pi)
			p.y = self.state.central.y + self.length / 2 * sin((self.state.alpha1-180)/180*pi)
		if idx == 6:
			p.x = self.state.central.x + self.length / 2 * cos((self.state.alpha1-180)/180*pi) + self.width / 2 * cos((self.state.alpha1-90)/180*pi)
			p.y = self.state.central.y + self.length / 2 * sin((self.state.alpha1-180)/180*pi) + self.width / 2 * sin((self.state.alpha1-90)/180*pi)
		if idx == 7:
			p.x = self.state.central.x
			p.y = self.state.central.y
		return p


	def show(self):
		print("Vị trí:")
		self.state.show()
		print("Tốc độ",self.speed)
		print('~'*30)
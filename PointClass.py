import copy

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def dist(self,p):
		return ((self.x - p.x)**2+(self.y - p.y)**2)**0.5

	def show(self):
		print(self.x,self.y)

class Polygon:
	numberOfPoint = 0
	pointList = []
	def __init__(self,pointList):
		self.numberOfPoint = len(pointList)
		self.pointList = [point for point in pointList]

	def show(self):
		print("Số điểm",self.numberOfPoint,":")
		for point in self.pointList:
			point.show()

	def listType(self):
		return [(point.x,point.y) for point in self.pointList]

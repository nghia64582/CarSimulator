from PointClass import *

# lớp State lưu 3 thông số
# central: tọa độ tâm một chiếc xe
# alpha1: lưu góc giữa trục xe và trục Ox
# alpha2: lưu góc quay bánh xe

class State:
	def __init__(self,central,alpha1,alpha2):
		self.central = central
		self.alpha1 = alpha1
		self.alpha2 = alpha2

	def isCollision(self,polygon):
		pass

	def show(self):
		print("Tọa độ:",round(self.central.x % 360,3),round(self.central.y % 360,3))
		print("Góc alpha 1:",self.alpha1)
		print("Góc alpha 2:",self.alpha2)

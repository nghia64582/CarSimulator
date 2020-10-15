import pygame
from PointClass import *

# draw point and polygon and line with a reference system

screenHeight = 700
screenWidth = 1300

def drawPolygon(screen,color,polygon,thickness,referSystem):
	polygon = Polygon([Point(point.x*referSystem.zoom+referSystem.p.x,point.y*referSystem.zoom+referSystem.p.y) for point in polygon.pointList])
	polygon = [(point.x,screenHeight - point.y) for point in polygon.pointList]
	pygame.draw.polygon(screen,color,polygon,thickness)

def drawPoint(screen,color,point,thickness,referSystem):
	point.x = point.x * referSystem.zoom + referSystem.p.x
	point.y = point.y * referSystem.zoom + referSystem.p.y
	pygame.draw.rect(screen,color,[point.x-2,screenHeight-(point.y+2),4,4],thickness)

def drawEllipse(screen,color,rect,referSystem):
	rect = [i*zoom for i in rect]
	pygame.draw.ellipse(screen,color,rect)
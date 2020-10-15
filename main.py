import pygame
import sys
from time import *
from math import *
from random import *
from copy import *
from VehicleClass import *
from StateClass import *
from PointClass import *
from Color import *
from Draw import *
from ReferSystem import *

def initInformation():
	global myVehicle,referSystem,thickness,accelebration,reverseMode,obstacleList,parkingZone
	# init my vehicle
	coor = Point(0,5)
	state = State(coor,0,0)
	speed = 0
	myVehicle = Vehicle(state,speed,blue)
	# init reference system
	zoom = 20
	root = Point(400,100)
	referSystem = ReferSystem(root,zoom)
	# init information
	thickness = 2
	accelebration = 1
	reverseMode = False
	# init obstacle's list
	obstacleList = []
	for i in range(10):
		x=randint(1,30)
		y=randint(1,30)
		obstacleList.append(Polygon([Point(x,y),Point(x+1,y),Point(x+1,y+1),Point(x,y+1)]))
	obstacleList.append(Polygon([Point(0,0),Point(0,2),Point(4,2),Point(4,0)]))
	obstacleList.append(Polygon([Point(10,0),Point(10,2),Point(14,2),Point(14,0)]))
	parkingZone = Polygon([Point(5,0),Point(5,2),Point(9,2),Point(9,0)])


def processEvent(event):
	global running,accelebration,reverseMode
	ESCAPECODE = 27
	if event.type == pygame.QUIT:
		running = False
	if event.type == pygame.KEYDOWN:
		# print(event.key)
		if event.key == ESCAPECODE:
			running = False
		elif event.key == ord('s'):
			# slow down
			myVehicle.speed -= accelebration
			if not reverseMode and myVehicle.speed < 0:
				myVehicle.speed = 0.001
		elif event.key == ord('w'):
			myVehicle.speed += accelebration
			if reverseMode and myVehicle.speed > 0:
				myVehicle.speed = 0.001
		elif event.key == ord('a'):
			myVehicle.state.alpha2 += 5 # randint(4,6)
		elif event.key == ord('d'):
			myVehicle.state.alpha2 -= 5 # randint(4,6)
		elif event.key == ord('z'):
			referSystem.zoom /= randint(14,16)/10
		elif event.key == ord('c'):
			referSystem.zoom *= randint(14,16)/10
		elif event.key == ord('q'):
			accelebration /= 1.5
		elif event.key == ord('e'):
			accelebration *= 1.5
		elif event.key == ord('.'):
			myVehicle.show()
		elif event.key == ord(' '):
			myVehicle.show()
		elif event.key == ord('r'):
			reverseMode = not reverseMode

def drawInfo():
	speedText = font.render("Speed            :"+str(round(myVehicle.speed,2))+' m/s',True,white)
	screen.blit(speedText,(10,10))
	acceText = font.render("Accelebration  :"+str(round(accelebration,2))+' m/s2',True,white)
	screen.blit(acceText,(10,40))
	radius = myVehicle.length * tan((90 - myVehicle.state.alpha2) / 180 * pi) if myVehicle.state.alpha2 % 360 > 1e-2 else 0
	radiusText = font.render("Turning radius:"+str(round(radius,2))+' m',True,white)
	screen.blit(radiusText,(10,70))
	reverseModeText = font.render("Reverse Mode:" + ("On" if reverseMode else "Off"),True,white)
	screen.blit(reverseModeText,(10,100))
	alpha2Text = font.render("Turning angle (o):" + str(myVehicle.state.alpha2)[:5] ,True,white)
	screen.blit(alpha2Text,(10,130))
	timeText = font.render(str(round(time()-startTime,2))+' s',True,white)
	screen.blit(timeText,(10,160))

def drawObstacle():
	for obstacle in obstacleList:
		drawPolygon(screen,blue,obstacle,thickness,referSystem)

def drawParkingzone():
	### 
	drawPolygon(screen,yellow,parkingZone,thickness,referSystem)

def drawReferenceSystem():
	drawPolygon(screen,red,Polygon([Point(-100,0),Point(100,0)]),thickness,referSystem)
	drawPolygon(screen,red,Polygon([Point(0,-100),Point(0,100)]),thickness,referSystem)

def drawPredictedPosition():
	# draw position of car in next several seconds
	# case 1 : positive speed - draw p1 and p3
	# case 2 : negative speed - draw p4 and p6
	# case 3 : zero speed - draw p1 p3 p4 p5 with 1 m/s speed
	numberOfPosition = 30
	timeBetweenEachPosition = 0.5

	if abs(myVehicle.speed) < 0.01:
		myVehicle.speed = 1
		for i in range(-numberOfPosition,0):
			preState = deepcopy(myVehicle.state)
			myVehicle.state = myVehicle.nextPosition(i*timeBetweenEachPosition)
			p1 = myVehicle.pointInVehicle(4)
			p2 = myVehicle.pointInVehicle(6)
			drawPoint(screen,white,p1,1,referSystem)
			drawPoint(screen,white,p2,1,referSystem)
			myVehicle.state = preState
		for i in range(1,numberOfPosition+1):
			preState = deepcopy(myVehicle.state)
			myVehicle.state = myVehicle.nextPosition(i*timeBetweenEachPosition)
			p1 = myVehicle.pointInVehicle(1)
			p2 = myVehicle.pointInVehicle(3)
			drawPoint(screen,white,p1,1,referSystem)
			drawPoint(screen,white,p2,1,referSystem)
			myVehicle.state = preState

		myVehicle.speed = 0

	for i in range(1,numberOfPosition+1):
		preState = deepcopy(myVehicle.state)
		myVehicle.state = myVehicle.nextPosition(i*timeBetweenEachPosition)
		if myVehicle.speed > 0:
			p1 = myVehicle.pointInVehicle(1)
			p2 = myVehicle.pointInVehicle(3)
		else:
			p1 = myVehicle.pointInVehicle(4)
			p2 = myVehicle.pointInVehicle(6)
		drawPoint(screen,white,p1,1,referSystem)
		drawPoint(screen,white,p2,1,referSystem)
		myVehicle.state = preState
	
def drawVehicle():
	# draw my vehicle
	drawPolygon(screen,green,myVehicle.polygonShape(),thickness,referSystem)

def drawScreen():
	screen.fill(black)
	drawInfo()
	drawObstacle()
	drawVehicle()
	drawReferenceSystem()
	drawParkingzone()
	drawPredictedPosition()
	pygame.display.update()

def eventProcessing():
	for event in pygame.event.get():
		processEvent(event)

def actionEachLoop():
	myVehicle.move(0.05)
	myVehicle.speed *= 0.998
	# myVehicle.state.alpha2 *= 1 - min(0.01,abs(myVehicle.speed)/1000)

pygame.init()
initInformation()
screen = pygame.display.set_mode((screenWidth,screenHeight))
running = True
font = pygame.font.SysFont('Times New Roman',30)
startTime = time()
while running:
	# start = time()
	eventProcessing()
	actionEachLoop()
	referSystem.centralize(myVehicle.state.central)
	drawScreen()
	sleep(0.03)
	# print(1/(time()-start))

pygame.quit()
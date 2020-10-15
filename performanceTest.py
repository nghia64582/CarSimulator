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


coor = Point(0,0)
state = State(coor,10,20)
speed = 5
start = time()
myVehicle = Vehicle(state,speed,blue)
for i in range(10000):
	t = randint(1,1000) / 10
	s = myVehicle.nextPosition(t)

print('States per second:',round(10000/(time()-start),2))
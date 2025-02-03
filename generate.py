import pyrosim.pyrosim as pyrosim
import time

length = 1
width = 1
height = 1

x =-3
y = -2
z = 0.5

pyrosim.Start_SDF("boxes.sdf")

for j in range(0,5):
    y = y+1
    x = -3
    for k in range(0,5):
        x = x+1
        length = 1
        width = 1
        height =1
        for i in range(0,10):
            
            pyrosim.Send_Cube(name="Box", pos=[x,y,z+i] , size=[length,width,height])
            length = .9*length
            width = .9*width
            height = .9*height

#pyrosim.Send_Cube(name="Box2", pos=[x+1,y,z+1] , size=[length,width,height])






pyrosim.End()


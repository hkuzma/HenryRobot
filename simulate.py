#Henry Kuzma    
import pybullet as p
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random
import matplotlib.pyplot as m
import constants as c
from simulation import SIMULATION






sim = SIMULATION()
sim.run()










#find plane.urdf
import pybullet_data



physicsClient = p.connect(p.GUI)

#find plane.urdf
p.setAdditionalSearchPath(pybullet_data.getDataPath())




#add gravity
p.setGravity(c.GRAVITY_X,c.GRAVITY_Y,c.GRAVITY_Z)


#add da floor
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")




#Simulate Box from pyrosim
p.loadSDF("world.sdf")

#Prep for sensors
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(c.RUNTIME)
frontLegSensorValues = numpy.zeros(c.RUNTIME)



frontMotorVector = numpy.linspace(c.NUMPY_START, c.NUMPY_STOP, c.RUNTIME)
front_target_angles = c.amplitude * numpy.sin(c.frequency*frontMotorVector + c.phaseOffset)


backMotorVector = numpy.linspace(c.NUMPY_START, c.NUMPY_STOP, c.RUNTIME)
back_target_angles = c.amplitude2 * numpy.sin(c.frequency2*backMotorVector + c.phaseOffset2)


for i in range(c.RUNTIME):
    
    
    #Interesting stuff
    #======================================================================================
    #Scale to pi/4
    #target_angles[i] = target_angles[i] * (numpy.pi/4)
    #target_angles[i] = target_angles[i] * amplitude*(numpy.sin(frequency* i + phaseOffset))

    
    
    p.stepSimulation()
    #Add touch sensor to backleg
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, 
                                jointName = b"Torso_BackLeg",
                                controlMode = p.POSITION_CONTROL,
                                targetPosition = back_target_angles[i],
                                maxForce = c.MAXFORCE)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, 
                                jointName = b"Torso_FrontLeg",
                                controlMode = p.POSITION_CONTROL,
                                targetPosition = front_target_angles[i],
                                maxForce = c.MAXFORCE)


    time.sleep(c.SLEEPTIME)
    #print(i)
    print(front_target_angles[i])
    
    




p.disconnect()

numpy.save("data\\front_target_angles", front_target_angles)
numpy.save("data\\back_target_angles", back_target_angles)

numpy.save("data\\backLegSensorValues.npy", backLegSensorValues)
numpy.save("data\\frontLegSensorValues.npy", frontLegSensorValues)



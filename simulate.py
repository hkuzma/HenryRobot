#Henry Kuzma    
import pybullet as p
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random
import matplotlib.pyplot as m




RUNTIME = 1000

amplitude = numpy.pi/4
frequency = 20
phaseOffset = 0

amplitude2 = numpy.pi/2
frequency2 = 10
phaseOffset2 = 0

#find plane.urdf
import pybullet_data



physicsClient = p.connect(p.GUI)

#find plane.urdf
p.setAdditionalSearchPath(pybullet_data.getDataPath())


#p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)


#add gravity
p.setGravity(0,0,-9.8)

#add da floor
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")




#Simulate Box from pyrosim
p.loadSDF("world.sdf")

#Prep for sensors
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(RUNTIME)
frontLegSensorValues = numpy.zeros(RUNTIME)



frontMotorVector = numpy.linspace(0, 2 * numpy.pi, RUNTIME)
front_target_angles = amplitude * numpy.sin(frequency*frontMotorVector + phaseOffset)


backMotorVector = numpy.linspace(0, 2 * numpy.pi, RUNTIME)
back_target_angles = amplitude2 * numpy.sin(frequency2*backMotorVector + phaseOffset2)


for i in range(RUNTIME):
    
    
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
                                maxForce = 30)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, 
                                jointName = b"Torso_FrontLeg",
                                controlMode = p.POSITION_CONTROL,
                                targetPosition = front_target_angles[i],
                                maxForce = 30)


    time.sleep(1/60)
    #print(i)
    print(front_target_angles[i])
    
    




p.disconnect()

numpy.save("data\\front_target_angles", front_target_angles)
numpy.save("data\\back_target_angles", back_target_angles)

numpy.save("data\\backLegSensorValues.npy", backLegSensorValues)
numpy.save("data\\frontLegSensorValues.npy", frontLegSensorValues)



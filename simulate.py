#Henry Kuzma    
import pybullet as p
import time

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



#Simulate Box from pyrosim
p.loadSDF("boxes.sdf")


    
for i in range(0,100000):
    p.stepSimulation()
    time.sleep(1/60)
    print(i)
    
    


p.disconnect()
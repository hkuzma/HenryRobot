from world import WORLD
from robot import ROBOT
import pybullet_data
import pybullet as p
import constants as c
import pyrosim.pyrosim as pyrosim
import time



class SIMULATION:
    
    def __init__(self):
        
        simulation = SIMULATION
        
        
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAVITY_X,c.GRAVITY_Y,c.GRAVITY_Z)
        
        
        self.world = WORLD()
        self.robot = ROBOT()
        
        
     
        
        
    def __del__(self):
        p.disconnect()

         
    def run(self):
                
        for i in range(c.RUNTIME):
            
            self.robot.Sense(i)
            self.robot.act(i)

            time.sleep(c.SLEEPTIME)
           
        


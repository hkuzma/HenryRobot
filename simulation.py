from world import WORLD
from robot import ROBOT
import pybullet_data
import pybullet as p
import constants as c
import pyrosim.pyrosim as pyrosim
import time



class SIMULATION:
    
    def __init__(self, DIRECT, solutionID):
        
        simulation = SIMULATION
        
        self.directOrGUI = DIRECT
        
        if DIRECT == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAVITY_X,c.GRAVITY_Y,c.GRAVITY_Z)
        
        
        
       



        self.robot = ROBOT(solutionID)
        self.world = WORLD()
        
       
            
    def __del__(self):
        p.disconnect()
 
    def run(self):
                
        for i in range(c.RUNTIME):
            
            p.stepSimulation()
            
            self.robot.Sense(i)
            
            self.robot.Think()

            self.robot.act(i)
            
            if self.directOrGUI == "DIRECT":
                pass
            else:
                time.sleep(c.SLEEPTIME)
            
    def Get_Fitness(self):
        self.robot.Get_Fitness()
            
           
        


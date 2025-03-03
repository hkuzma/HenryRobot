from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim

class ROBOT:
    
    def __init__(self):
        
        robot = ROBOT
        
        self.robotId = p.loadURDF("body.urdf")

        
        pyrosim.Prepare_To_Simulate(self.robotId)
        robot.Prepare_To_Sense(self)
        robot.Prepare_To_Act(self)
        
        
    def Prepare_To_Sense(self):
        self.sensors = {}
        
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
            
    def Sense(self, t):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(t)
            
    def Prepare_To_Act(self):
        self.motors = {}
        
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
            
    def act(self, t):
        for jointName in self.motors:
            self.motors[jointName].Set_Value(self, t)
            
    
            
            
            

        
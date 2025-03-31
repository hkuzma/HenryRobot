from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c



class ROBOT:
    
    def __init__(self, solutionID):
        
        robot = ROBOT
        
        self.solutionID = solutionID
        
        self.robotId = p.loadURDF("body.urdf")
        
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        
        pyrosim.Prepare_To_Simulate(self.robotId)
        robot.Prepare_To_Sense(self)
        robot.Prepare_To_Act(self)
        
        os.system(f"del brain{self.solutionID}.nndf")
        
        
        
        
        
    def Prepare_To_Sense(self):
        self.sensors = {}
        
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
            
    def Sense(self, t):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(t)
            
    def Think(self):
        self.nn.Update()
        #self.nn.Print()   
            
    def Prepare_To_Act(self):
        self.motors = {}
        
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
            
    def act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode('utf-8')
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange

                self.motors[jointName].Set_Value(self, desiredAngle)

    def Get_Fitness(self):
        self.stateOfLinkZero = p.getLinkState(self.robotId,0)
        
        self.positionOfLinkZero = self.stateOfLinkZero[0]
        
        self.xCoordinateOfLinkZero = self.positionOfLinkZero[0]
        
        f = open(f"tmp{self.solutionID}.txt", "w")
        f.write(f"{self.xCoordinateOfLinkZero}")
        f.close()
        os.system(f"rename tmp{self.solutionID}.txt fitness{self.solutionID}.txt")


                
        
            
         
    
            
            
            

        
from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import numpy as n



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
        
        self.zPositions = []
        
        
        
        
        
    def Prepare_To_Sense(self):
        self.sensors = {}
        
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
            
    def Sense(self, t):
        #print(self.sensors)
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(t)
            
    def Think(self):
        self.nn.Update()
        
        
        
        self.stateOfLinkZero = p.getLinkState(self.robotId,0)
        self.positionOfLinkZero = self.stateOfLinkZero[0]
        self.zPosition = self.positionOfLinkZero[2]
        self.zPositions.append(self.zPosition)
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
        self.basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        
        
        #print(self.nn.Get_Neuron_Names())
        5/6
        #print(self.sensors.keys())
        
        BackFoot = n.average(self.sensors['BackFoot'].Get_Values())
        FrontFoot = n.average(self.sensors['FrontFoot'].Get_Values())
        Torso = n.average(self.sensors["Torso"].Get_Values())
        BackLeg = n.average(self.sensors["BackLeg"].Get_Values())
        FrontLeg = n.average(self.sensors["FrontLeg"].Get_Values())
        


        
        
        self.positionOfLinkZero = self.stateOfLinkZero[0]
        self.basePosition = self.basePositionAndOrientation[0]
        
        self.xCoordinateOfLinkZero = self.positionOfLinkZero[0]
        
        #self.zPosition = self.basePosition[2]  #WHAT IS THIS RETURNING???
        
        #SETS Y POSITION TO 1 TIME MAXIMAL POS
        #self.zPositions.append(self.zPosition)
        
        z_avg = n.average(self.zPositions)
        minimum = min(self.zPositions)
        # if minimum <.85:
        #     minimum = 100
        
        fitness = (15*BackFoot + 15*FrontFoot + Torso + 5*BackLeg + 5*FrontLeg)/5 + max(self.zPositions)
        print(z_avg)
        print(max(self.zPositions))
        print(f"MIN: {min(self.zPositions)}")

        
        f = open(f"tmp{self.solutionID}.txt", "w")
        f.write(f"{fitness}")
        f.close()
        os.system(f"rename tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
        


                
        
            
         
    
            
            
            

        
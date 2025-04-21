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
        self.RFPositions = []
        self.LFPositions = []
        
        self.LeftLowerLegZpositions = []
        self.RightLowerLegZpositions = []
        self.LeftFootZpositions = []
        self.RightFootZpositions = []
        self.zlinearvels = []
        
        
        
        
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
        
        
        
        self.stateOfLinkZero, orn = p.getBasePositionAndOrientation(self.robotId)
        self.zPosition = self.stateOfLinkZero[2]
        self.zPositions.append(self.zPosition)
        
        linear_vel, angular_vel = p.getBaseVelocity(self.robotId)
        zlinvel = linear_vel[2]
        
        
        self.stateOfRightFist = p.getLinkState(self.robotId,3)
        self.positionOfRightFist = self.stateOfRightFist[0]
        self.RFPosition = self.positionOfRightFist[2]
        self.RFPositions.append(self.zPosition)
        
        self.stateOfLeftFist = p.getLinkState(self.robotId,1)
        self.positionOfLeftFist = self.stateOfLeftFist[0]
        self.LFPosition = self.positionOfLeftFist[2]
        self.LFPositions.append(self.LFPosition)

        self.stateOfLeftLowerLeg = p.getLinkState(self.robotId,7)
        self.positionOfLeftLowerLeg = self.stateOfLeftLowerLeg[0]
        self.LeftLowerLegZpos = self.positionOfLeftLowerLeg[2]
        self.LeftLowerLegZpositions.append(self.LeftLowerLegZpos)

        self.stateOfRightLowerLeg = p.getLinkState(self.robotId,8)
        self.positionOfRightLowerLeg = self.stateOfRightLowerLeg[0] 
        self.RightLowerLegZpos = self.positionOfRightLowerLeg[2]
        self.RightLowerLegZpositions.append(self.RightLowerLegZpos)
        
        self.stateOfLeftFoot = p.getLinkState(self.robotId, 6)
        self.positionOfLeftFoot = self.stateOfLeftFoot[0] 
        self.LeftFootZpos = self.positionOfLeftFoot[2]
        self.LeftFootZpositions.append(self.RightLowerLegZpos)
        
        self.stateOfRightFoot = p.getLinkState(self.robotId, 9)
        self.positionOfRightFoot = self.stateOfRightFoot[0] 
        self.RightFootZpos = self.positionOfRightFoot[2]
        self.RightFootZpositions.append(self.RightFootZpos)
        
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
        
        #UPPPER ARM
        LeftUpperArm = self.sensors["LeftUpperArm"].Get_Values()
        RightUpperArm = self.sensors["RightUpperArm"].Get_Values()
        #LOWER ARM
        # LeftLowerArm = self.sensors["LeftLowerArm"].Get_Values()
        # RightLowerArm = self.sensors["RightLowerArm"].Get_Values()
        #FIST
        RightFist = self.sensors["RightFist"].Get_Values()
        LeftFist = self.sensors["LeftFist"].Get_Values()
        #TORSO
        Torso = self.sensors["Torso"].Get_Values()
        #UPPER LEG
        LeftUpperLeg = self.sensors['BackLeg'].Get_Values()
        RightUpperLeg = self.sensors['FrontLeg'].Get_Values()
        #LOWER LEG
        LeftLowerLeg = self.sensors['BackLowerLeg'].Get_Values()
        RightLowerLeg = self.sensors['FrontLowerLeg'].Get_Values()
        #FOOT
        LeftFoot = self.sensors['BackFoot'].Get_Values()
        RightFoot = self.sensors['FrontFoot'].Get_Values()
        
        maxLeftFootHeight = max(self.LeftFootZpositions)
        maxRightFootHeight = max(self.RightFootZpositions)
        maxLeftLegHeight = max(self.LeftLowerLegZpositions)
        maxRightLegHeight = max(self.RightLowerLegZpositions)
        
        
        maxHeight = max(self.zPositions)
        minHeight = min(self.zPositions)
        avgHeight = n.average(self.zPositions)
        
        maxLFHeight = max(self.LFPositions)
        minLFHeight = min(self.LFPositions)
        avgLFHeight = n.average(self.LFPositions)
        
        maxRFHeight = max(self.RFPositions)
        minRFHeight = min(self.RFPositions)
        avgRFHeight = n.average(self.RFPositions)
        
        self.positionOfLinkZero = self.stateOfLinkZero[0]
        self.basePosition = self.basePositionAndOrientation[0]
        
        self.xCoordinateOfLinkZero = self.positionOfLinkZero[0]
        
        #self.zPosition = self.basePosition[2]  #WHAT IS THIS RETURNING???
        #SETS Y POSITION TO 1 TIME MAXIMAL POS
        #self.zPositions.append(self.zPosition)
        
        z_avg = n.average(self.zPositions)
        minimum = min(self.zPositions)
        # if minimum <.85:
        # minimum = 100
        
        
        fitness = 0
        indexes = []
        fisttouch = False
        for i in range(len(LeftFoot)):
            if LeftFoot[i] == -1 and RightFoot[i] == -1 and LeftLowerLeg[i] == -1 and RightLowerLeg[i] == -1 and Torso[i] ==-1 and LeftFist[i] == -1 and RightFist[i] == -1:
                fitness += 1
                indexes.append(i)
            if RightFist[i] == 1 or LeftFist[i] == 1:
                fisttouch = True
        
        maxSequence = 0      
        sequence = 0
        sequences = []
        for i in range(1, len(indexes)):
            if indexes[i] == indexes[i-1] + 1:
                sequence += 1
            elif sequence > maxSequence:
                maxSequence = sequence
                sequences.append(sequence)
                sequence = 0
            elif sequence > 3:
                sequences.append(sequence)
                sequence = 0
            else:
                sequence = 0
        
        #SEQUENCE FITNESS
        #fitness is based on longest sequence where all links off ground
        #fitness maxes out around 3.25
        #===========================================================================================================
        fitness = 10*maxSequence + maxHeight
        # if fisttouch:
        #     fitness = 0
        f = open("SEQUENCE FITNESS.txt", 'a')
        f.write(f"{'{'}\nMAX SEQUENCE: {maxSequence}\n MAX HEIGHT: {maxHeight}\n MIN RF HEIGHT: {minRFHeight}\n MIN LF HEIGHT: {minLFHeight}\n {'}'}")
        f.close()
        
        
        #fitness based on maximum heights of two feet
        #===========================================================================================================
        #fitness = maxRFHeight + maxLFHeight
        

        # f = open("FEET HEIGHT FITNESS, ", 'a')
        # f.write(f"{'{\n'}MAX RF HEIGHT: {maxRFHeight}\n MAX LF HEIGHT: {maxLFHeight}")
        # f.close()
        
        #===========================================================================================================
        
        num_joints = p.getNumJoints(self.robotId)

        f = open("JOINT INFO.txt", 'w')
        
        for i in range(num_joints):
            joint_info = p.getJointInfo(self.robotId, i)
            f.write(f"Index: {i}, Link Name: {joint_info[12].decode('utf-8')}\n")
        f.close()
        
        #fitness = (-1*Torso + -1*BackLeg + -1*FrontLeg + -1*RightFist + -1*LeftFist)/5 + max(self.zPositions) + min(self.RFPositions) + min(self.LFPositions)
        # if min(self.zPositions) < 1:
        #     fitness = 0
        print(z_avg)
        print(max(self.zPositions))
        print(f"MIN: {min(self.zPositions)}")
        print(self.zPositions[0])

        
        f = open(f"tmp{self.solutionID}.txt", "w")
        f.write(f"{fitness}")
        f.close()
        os.system(f"rename tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
        


                
        
            
         
    
            
            
            

        
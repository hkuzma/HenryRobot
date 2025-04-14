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
        self.BackLowerLegZpositions = []
        self.FrontLowerLegZpositions = []
        self.LeftLowerLegZpositions = []
        self.RightLowerLegZpositions = []
        
        
        
        
        
        
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
        
        self.stateOfBackLowerLeg = p.getLinkState(self.robotId,1)
        self.positionOfBackLowerLeg = self.stateOfBackLowerLeg[0]
        self.BackLowerLegZpos = self.positionOfBackLowerLeg[2]
        self.BackLowerLegZpositions.append(self.BackLowerLegZpos)

        
        self.stateOfFrontLowerLeg = p.getLinkState(self.robotId,3)
        self.positionOfFrontLowerLeg = self.stateOfFrontLowerLeg[0]
        self.FrontLowerLegZpos = self.positionOfFrontLowerLeg[2]
        self.FrontLowerLegZpositions.append(self.FrontLowerLegZpos)

        self.stateOfLeftLowerLeg = p.getLinkState(self.robotId,5)
        self.positionOfLeftLowerLeg = self.stateOfLeftLowerLeg[0]
        self.LeftLowerLegZpos = self.positionOfLeftLowerLeg[2]
        self.LeftLowerLegZpositions.append(self.LeftLowerLegZpos)

        self.stateOfRightLowerLeg = p.getLinkState(self.robotId,7)
        self.positionOfRightLowerLeg = self.stateOfRightLowerLeg[0] 
        self.RigthLowerLegZpos = self.positionOfRightLowerLeg[2]
        self.RightLowerLegZpositions.append(self.RigthLowerLegZpos)



            
    def Prepare_To_Act(self):
        self.motors = {}
        
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
            
    def act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode('utf-8')
                if "Lower" in str(jointName):
                    desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                else:
                    desiredAngle = self.nn.Get_Value_Of(neuronName) * ( c.motorJointRange)

                self.motors[jointName].Set_Value(self, desiredAngle)

    def Get_Fitness(self):
        self.stateOfLinkZero = p.getLinkState(self.robotId,0)
        self.basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        
        
        #print(self.nn.Get_Neuron_Names())
        5/6
        #print(self.sensors.keys())
        
        #FIND MAXIMUM HEIGHT OF EACH LEG
        maxLeg1Height = max(self.BackLowerLegZpositions)
        maxLeg2Height = max(self.FrontLowerLegZpositions)
        maxLeg3Height = max(self.LeftLowerLegZpositions)
        maxLeg4Height = max(self.RightLowerLegZpositions)
        
        maxHeight = max(self.zPositions)
        
        

        
        
        
        # LEGHEIGHT = maxLeg1Height-1 + maxLeg2Height-1 + maxLeg3Height-1 + maxLeg4Height-1
        
        #FIND AVERAGE OF TOUCH SENSOR VALUES
        BackFoot = self.sensors['BackLowerLeg'].Get_Values()
        FrontFoot = self.sensors['FrontLowerLeg'].Get_Values()
        #Torso = n.average(self.sensors["Torso"].Get_Values())
        RightFoot = self.sensors["RightLowerLeg"].Get_Values()
        LeftFoot = self.sensors["LeftLowerLeg"].Get_Values()
        
        BackFootHeights = self.BackLowerLegZpositions
        FrontFootHeights = self.FrontLowerLegZpositions
        LeftFootHeights = self.LeftLowerLegZpositions
        RightFootHeights = self.RightLowerLegZpositions
        
        # print(f"BACKFOOT{BackFoot[20]}")
        
        # BackFootSenses = [BackFoot[20]]
        # FrontFootSenses = [FrontFoot[20]]
        # LeftFootSenses = [LeftFoot[20]]
        # RightFootSenses = [RightFoot[20]]
        
        
        #HOW TO FIND LONGEST TIME OFF GROUND???
        
        
        # self.positionOfLinkZero = self.stateOfLinkZero[0]
        # self.basePosition = self.basePositionAndOrientation[0]
        
        # self.xCoordinateOfLinkZero = self.positionOfLinkZero[0]
        
        #self.zPosition = self.basePosition[2]  #WHAT IS THIS RETURNING???
        
        #SETS Y POSITION TO 1 TIME MAXIMAL POS
        #self.zPositions.append(self.zPosition)
        
        # z_avg = n.average(self.zPositions)
        # minimum = min(self.zPositions)
        # maximum = max(self.zPositions)
        # if minimum <.85:
        #     minimum = 100
        
        # fitness = 0
        # for i in range(0,10):
        #     # if BackFoot[20+i] == -1 and FrontFoot[20+i] == -1 and LeftFoot[20+i] == -1 and RightFoot[20+i] == -1:
        #     #     fitness+=1
        #     if BackFootHeights[20+i] > .52 and FrontFootHeights[20+i] > .52 and LeftFootHeights[20+i] >.52 and RightFootHeights[20+i] >.52:
        #         fitness+= BackFootHeights[20+i]
        #     else:
        #         elseFIT =  f"{(max(BackFootHeights[20:30]) -.55)}, {(max(FrontFootHeights[20:30]) -.55)}, {(max(LeftFootHeights[20:30]) -.55)}, {(max(RightFootHeights[20:30]) -.55)}"
        #         fitness += (max(BackFootHeights[20:30]) -.55) + (max(FrontFootHeights[20:30]) -.55) + (max(LeftFootHeights[20:30]) -.55) + (max(RightFootHeights[20:30]) -.55)
            

        
        #fitness = (BackFoot + FrontFoot + LeftFoot + RightFoot)/4 + LEGHEIGHT + 5*(maximum - minimum) + maximum
        fitness = ((((-1* BackFoot[20]) * (-1 * RightFoot[20])) * (-1* FrontFoot[20])) * (-1*LeftFoot[20]) +
                   (((-1* BackFoot[21]) * (-1 * RightFoot[21])) * (-1* FrontFoot[21])) * (-1*LeftFoot[21]) +
                   (((-1* BackFoot[22]) * (-1 * RightFoot[22])) * (-1* FrontFoot[22])) * (-1*LeftFoot[22])                                                                                         )
                  
        # print(max(self.zPositions))
        # print(f"MIN: {min(self.zPositions)}")
        
    #MAXIMIZES TIME STEPS IN A ROW WHERE ALL 4 LEGS ARE OFF THE GROUND
    #PERVERSE INSTANTIATION:: SOMETIMES ROBOT GETS ALL 4 TOUCH SENSORS OFF THE GROUND BY STANDING ON IT's TIPPY TOES
        #Find all time steps where all 4 legs of ground
        fitness = 0
        indexes = []
        for i in range(len(BackFoot)):
            if BackFoot[i] == -1 and FrontFoot[i] == -1 and LeftFoot[i] == -1 and RightFoot[i] == -1:
                fitness += 1
                indexes.append(i)
        
        #Determine how many of these time steps are in a row
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
         
      
                
        
        
        #fitness = 5*maxSequence + len(sequences)
        fitness = maxSequence + ((maxLeg1Height*2 + maxLeg2Height + maxLeg3Height*2 + maxLeg4Height)/4 *len(sequences))/5
        
        #CREATES MANY SMALL HOPS
        # fitness = (3*n.average(sequences))*len(sequences)

        #FITNESS FUNCTION LEADS TO TIP TAPPING ROBOT THAT MAKES MANY SMALL JUMPS
        #fitness = maxSequence + len(indexes)

        
        
        f = open(f"tmp{self.solutionID}.txt", "w")
        f.write(f"{fitness}")
        f.close()
        
        f = open("ROBOT LEG VALUES", 'a')
        #f.write(f"BACKFOOT: {BackFoot[20]}, FRONTFOOT: {FrontFoot[20]}, LEFTFOOT: {LeftFoot[20]}, RIGHTFOOT: {RightFoot[20]} || TOTAL {fitness} \n")
        f.write(f"INDEXES: {sequences} \n")
        f.write(f"MAXSEQUENCE: {maxSequence}")
        #f.write(f"\n{elseFIT}\n")
        f.close()
        os.system(f"rename tmp{self.solutionID}.txt fitness{self.solutionID}.txt")



                
        
            
         
    
            
            
            

        
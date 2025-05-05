from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import numpy as n
from statistics import mean


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
        
        
        self.stateOfLinkZero = p.getLinkState(self.robotId,0)
        self.positionOfLinkZero = self.stateOfLinkZero[0]
        self.zPosition = self.positionOfLinkZero[2]
        self.zPositions.append(self.zPosition)
        #self.nn.Print()   
        
        linear_vel, angular_vel = p.getBaseVelocity(self.robotId)
        zlinvel = linear_vel[2]
        self.zlinearvels.append(zlinvel)
        
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
        
        avgLegZPosies = []
        for index in range(0, len(self.BackLowerLegZpositions)):
            posAvg = (self.BackLowerLegZpositions[index]*self.FrontLowerLegZpositions[index]*self.LeftLowerLegZpositions[index]*self.RightLowerLegZpositions[index])**.25
            avgLegZPosies.append(posAvg)
            
        minLeg1Height = min(self.BackLowerLegZpositions)
        minLeg2Height = min(self.FrontLowerLegZpositions)
        minLeg3Height = min(self.LeftLowerLegZpositions)
        minLeg4Height = min(self.RightLowerLegZpositions)
        
        avgLeg1Height = n.average(self.BackLowerLegZpositions)
        avgLeg2Height = n.average(self.FrontLowerLegZpositions)
        avgLeg3Height = n.average(self.LeftLowerLegZpositions)
        avgLeg4Height = n.average(self.RightLowerLegZpositions)
        
        maxHeight = max(self.zPositions)
        minHeight = min(self.zPositions)
        
        

        
        
        
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
        SQjump = 0
        for i in range(1, len(indexes)):
            
            if indexes[i] == indexes[i-1] + 1:
                sequence += 1
                if self.zPositions[i]>SQjump:
                    SQjump == self.zPositions
                    
            elif sequence > maxSequence:
                maxSequence = sequence
                sequences.append(sequence)
                sequence = 0
            elif sequence > 3:
                sequences.append(sequence)
                sequence = 0
            else:
                sequence = 0
         
      
                
        
        #
        fitness = 5*maxSequence + len(sequences)
        
        
        
        
        
        #===================================================================================================================
        chain_values = []
        chain_indexes = []
        chain = 0
        chain_start =0 
        maxChain = 0
        max_chain_start = 0
        max_chain_end = 0
        for i in range(1,len(self.zPositions)):
            if self.zPositions[i-1] < self.zPositions[i]:
                chain_values.append(self.zPositions[i])
                chain_indexes.append(i)
        
        
        for i in range(1,len(chain_indexes)):
            if chain_indexes[i]-1 == chain_indexes[i-1]:
                chain_start = i
                chain +=1
            else:
                if chain > maxChain:
                    maxChain = chain
                    max_chain_start = chain_start
                    max_chain_end = i
                    
                    chain = 0
        
        deltaZ = self.zPositions[max_chain_end] - self.zPositions[max_chain_start]

        #1
        #Doesn't Jump Well
        fitness = max(self.zlinearvels) * deltaZ + maxHeight
        
        #2
        #Jumps
        #Holds up
        fitness = maxSequence * maxChain
        
        #3
        #Robot Gets Real Low
        fitness = maxSequence + maxChain * deltaZ
        
        #4
        #Almost Jumps
        fitness = min(maxLeg1Height, maxLeg2Height, maxLeg3Height, maxLeg4Height, maxHeight) * maxSequence
        
        #5
        #Small Jumps
        fitness = min(maxLeg1Height, maxLeg2Height, maxLeg3Height, maxLeg4Height, maxHeight) * maxSequence * maxChain
        
        #6
        #Bouncy but fails to jump        
        fitness = 5*maxSequence + len(sequences)
        
        #7
        #Does not jump
        fitness = min(maxLeg1Height, maxLeg2Height, maxLeg3Height, maxLeg4Height, maxHeight) * maxChain
        
        #8
        #Many Small Hops
        fitness = deltaZ * maxChain * maxSequence
        
        #9
        #1 solid jump + Several small jumps
        #less consistent
        fitness = max(self.zlinearvels) * maxChain * maxSequence
        
       
        total = 0
        for value in self.zlinearvels:
            value = abs(value)
            total += value
        
        avg = total/len(self.zlinearvels)
        
        #10
        #Maximizes height once and stays standing as tall as possible
        #Subsequent run --> Freezes after some movement --> Possibly avoiding any downwards velocity
        fitness = n.average(self.zlinearvels) * maxChain * maxSequence
        
        #11
        #By using the absolute value of linear velocity, we get some hops proving that the regular linear velocity prioritizes not going back down.
        fitness = avg * maxChain * maxSequence

        #12
        #revisiting number 1 using abs value of velocity shows that the problem there lies in the weight of delta z
        fitness = avg * deltaZ + maxHeight
        
        #13
        #Reducing the weight of deltaZ gives the best jump so far
        #on a second run, this jump failed to replicate --> Possible good luck???
        #maybe needs to run for longer?
        #running for longer could replicate better jumps, but the first time may have been a fluke.
        fitness = avg *maxHeight + deltaZ
        
        #14
        #performs significantly worse than above
        fitness = avg + maxHeight * deltaZ 
        
        #15
        #Performs better than above --> higher overall movement, but fails to jump on first run
        fitness = avg * maxHeight 
        
        #16
        #very effective at creating many jumps
        fitness = avg *maxHeight + maxChain * maxSequence
        
        


        #More sideways movement than upwards
        fitness = avg * maxChain * maxSequence
        
        #Jumps Down
        fitness = avg * maxChain * maxSequence + maxHeight*deltaZ
        
        #jumps but not high
        fitness = avg *maxHeight + deltaZ * maxChain
        
        
        
        fitness = avg *maxHeight + deltaZ
        
        
        #FITNESS FUNCTION WILL USE SEQUENCE
        deltaLeg = (maxLeg1Height- minLeg1Height +  maxLeg2Height- minLeg2Height +  maxLeg3Height- minLeg3Height +  maxLeg4Height- minLeg4Height)/4
        
        deltaLeg = (avgLeg1Height *  avgLeg2Height * avgLeg3Height * avgLeg4Height)**.25

        deltaLeg = n.average(avgLegZPosies)
        
        fitness = maxSequence * (maxHeight-minHeight)
        
        
        
        #VERY EFFECTIVE FITNESS FOR A ROBOT THAT HOPS MANY TIMES
        fitness = 5*maxSequence + deltaLeg + (maxHeight)
        
        indexes = []
        numFrames1 =0
        numFrames2 = 0
        for i in range(len(BackFoot)):
            if BackFoot[i] == -1 and FrontFoot[i] == -1 and LeftFoot[i] == -1 and RightFoot[i] == -1:
                pass
            if BackFoot[i] == 1 and FrontFoot[i] == 1 and LeftFoot[i] == -1 and RightFoot[i] == -1:
                numFrames1 +=1
            else:
                numFrames2 = 0
                
            if BackFoot[i] == -1 and FrontFoot[i] == -1 and LeftFoot[i] == 1 and RightFoot[i] == 1:
                numFrames2 +=1
            else:
                numFrames2 =0
            if numFrames1 >10:
                fitness -=2
            if numFrames2 > 10:
                fitness-=2
                
           
                
        
            



        
        
        






        #BEST
        #2
        #9
        #13

        
        

        
        
        
        
        #===================================================================================================================
        #fitness = maxSequence + (maxLeg1Height + maxLeg2Height + maxLeg3Height + maxLeg4Height)/4
        #fitness = maxSequence
        
        #CREATES MANY SMALL HOPS
        # fitness = (3*n.average(sequences))*len(sequences)

        #FITNESS FUNCTION LEADS TO TIP TAPPING ROBOT THAT MAKES MANY SMALL JUMPS
        #fitness = maxSequence + len(indexes)

        num_joints = p.getNumJoints(self.robotId)
        f = open("QUADJOINTINFO", 'w')
        for i in range(num_joints):
            info = p.getJointInfo(self.robotId, i)
            joint_name = info[1].decode('utf-8')
            child_link_name = info[12].decode('utf-8')
            f.write(f"Joint Index: {i}, Joint Name: {joint_name}, Child Link: {child_link_name}\n")
        
        f.close()
                
        
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



                
        
            
         
    
            
            
            

        
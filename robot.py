from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import numpy as n
import math


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
        
        
        
        #FITNESS
        self.zPositions = []
        self.RFPositions = []
        self.LFPositions = []
        
        self.LeftLowerLegZpositions = []
        self.RightLowerLegZpositions = []
        self.LeftFootZpositions = []
        self.RightFootZpositions = []
        self.zlinearvels = []
        
        self.backComps = []
        self.frontComps = []
        
        
        
        
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
        
        
        backcomp = self.motors[ b'BackLeg_BackLowerLeg'].Get_Value()
        self.backComps.append(backcomp)
        
        frontcomp = self.motors[ b'FrontLeg_FrontLowerLeg'].Get_Value()
        self.frontComps.append(frontcomp)

        
        
        self.stateOfLinkZero, orn = p.getBasePositionAndOrientation(self.robotId)
        self.zPosition = self.stateOfLinkZero[2]
        self.zPositions.append(self.zPosition)
        
        linear_vel, angular_vel = p.getBaseVelocity(self.robotId)
        zlinvel = linear_vel[2]
        self.zlinearvels.append(zlinvel)
        
        
        self.stateOfRightFist = p.getLinkState(self.robotId,3)
        self.positionOfRightFist = self.stateOfRightFist[0]
        self.RFPosition = self.positionOfRightFist[2]
        self.RFPositions.append(self.RFPosition)
        
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
        #Robot stands on its very heels
        #===========================================================================================================
        # fitness = min(maxRFHeight,maxLFHeight) * maxSequence
        

        # f = open("FEET HEIGHT FITNESS, ", 'a')
        # f.write(f"{'{'}\nMAX RF HEIGHT: {maxRFHeight}\n MAX LF HEIGHT: {maxLFHeight}\n MAX SEQUENCE: {maxSequence}")
        # f.close()
        
        #jumping is when i have the longest sequence where i keep getting higher 
        #jumping is when i do this ^^ but fast
        #===========================================================================================================


        chain_values = []
        chain_indexes = []
        
        
        #CHAIN GOING UP======================================>
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
                    
                
        
        jump_height = max(self.zPositions) - self.zPositions[0]
     
        deltaZ = self.zPositions[max_chain_end] - self.zPositions[max_chain_start]
        
        chainZVelocities = self.zlinearvels[max_chain_start:max_chain_end]
        RFchainpos = self.RFPositions[max_chain_start:max_chain_end]
        LFchainpos = self.LFPositions[max_chain_start:max_chain_end]
        
        
        #longest time the torso goes up + highest value for both feet during that time * highest upward velocity during that time 
        # * longest sequence off the ground + reward for getting off ground
        # fitness = (maxChain + 5*min(max(RFchainpos), max(LFchainpos))) + max(chainZVelocities) * (5*maxSequence) + 10*deltaZ
        
        
        #deltaZ = highest displacement during chain
        #POTENTIAL SOLUTION TO MAKE VERTICAL GROWTH?
        #fitness = deltaZ * max(chainZVelocities) * 1+(5*maxSequence)
        
     
        
        f = open("VELOCITIES", 'a')
        f.write(f"{'{'}\nMAX CHAIN: {maxChain}\n MAX VELOCITY {max(self.zlinearvels)}\n FITNESS: {fitness}\n{'}'}")
        f.close()    
        
        #KNEE COMPRESSION BONUS
        b'BackLeg_BackLowerLeg'
        b'FrontLeg_FrontLowerLeg'
        
        
        
        print(f"COMPRESSION = {max(self.frontComps)}")
        fitness = deltaZ

        # fitness += abs(max(self.frontComps[0:max_chain_start]))
        # fitness += abs(max(self.backComps[0:max_chain_start]))
        # fitness += ((minHeight-2.75)*-1) * (maxHeight-2.75)
        
        for value in Torso:
            if value == 1:
                fitness -= .1
            else:
                fitness += .1
                
                
                
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
        
    
        
        
        
        #6
        #Bouncy but fails to jump        
        fitness = 5*maxSequence + len(sequences)
    
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
        fitness = n.average(self.zlinearvels) * maxHeight + deltaZ * maxChain
        
        
        #fitness = min(abs(max(self.frontComps[0:max_chain_start])), abs(max(self.backComps[0:max_chain_start]))) * maxChain + avg
        
        
        #fitness = maxChain * avg + deltaZ + min(abs(max(self.frontComps[0:max_chain_start])), abs(max(self.backComps[0:max_chain_start])))
      
        
        
        
        
        
        
        
        
        
        #THE FULLY UPRIGHT BIPED CAN GET OFF THE GROUND
        #===============================================================================================================================
        
   
        
        avgZPosies = []
        for index in range(0, len(self.LeftLowerLegZpositions)):
            posAvg = (self.LeftLowerLegZpositions[index]* self.RightLowerLegZpositions[index]*self.LeftFootZpositions[index]*self.RightFootZpositions[index])**.25
            avgZPosies.append(posAvg)
        
        deltaLeg = n.average(avgZPosies)

        
        fitness = 5*maxSequence + deltaLeg + (maxHeight)
        
        indexes = []
        numFrames1 =0
        numFrames2 = 0

       
     
  
        #FOOT
        LeftFoot = self.sensors['BackFoot'].Get_Values()
        RightFoot = self.sensors['FrontFoot'].Get_Values()
        for i in range(len(Torso)):
            if Torso[i] == 1:
                fitness -=1
            if LeftUpperArm[i]==1 or RightUpperArm[i] == 1 or LeftUpperLeg[i]==1 or RightUpperLeg[i]==1:
                fitness -=.5
            if LeftFoot[i] == 1 or RightFoot[i] == 1:
                pass
            else: 
                fitness += 1
            
        
        
        
        num_joints = p.getNumJoints(self.robotId)

        #f = open("JOINT INFO.txt", 'w')
        
        # for i in range(num_joints):
        #     joint_info = p.getJointInfo(self.robotId, i)
        #     f.write(f"Index: {i}, Link Name: {joint_info[12].decode('utf-8')}\n")
        # f.close()
        
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
        


          
            
            
            

        
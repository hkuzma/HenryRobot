import numpy as np
import pyrosim.pyrosim as pyrosim
import time
import pyrosim.material as material
import random
import os
import constants as c

length = 1
width = 1
height = 1

robot_x =0
robot_y = 0
robot_z = 0.5

world_x = -3
world_y = 3
world_z = 0.5

class SOLUTION:
    
    def __init__(self, id):
        self.myID = id
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        self.weights = (self.weights *2 - 1)
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[world_x,world_y,world_z] , size=[length,width,height])
        pyrosim.End()
       
    
    def three_joint(self):
        #Added params to change color of link, will not work with source code for pyrosim!!!
        # color string follows format "0 1.0 1.0 1.0" (rgba)
        pyrosim.Start_URDF("body.urdf")
        #TORSO
        
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[0.5,width,height])
        #Backleg
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-.5,1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-.5,0] , size=[0.2,1,0.2], color="1.0 5 0.0 1.0", color_name="green")
        #BackLowerLeg
        pyrosim.Send_Joint(name = "BackLeg_BackLowerLeg", parent="BackLeg", child = "BackLowerLeg", type = "revolute", position= [0,-1,0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name = "BackLowerLeg", pos=[0,0,-.5] , size=[0.2,0.2,1], color="1.0 5 0.0 1.0", color_name="green")
        #Frontleg   
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,.5,1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name = "FrontLeg", pos=[0,.5,0] , size=[0.2,1,0.2], color="1.0 5 0.0 1.0", color_name="green")
        #FrontLowerLeg
        pyrosim.Send_Joint(name = "FrontLeg_FrontLowerLeg", parent="FrontLeg", child = "FrontLowerLeg", type = "revolute", position= [0,1,0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name = "FrontLowerLeg", pos=[0,0,-.5] , size=[0.2,0.2,1], color="1.0 5 0.0 1.0", color_name="green")
       
       
       
        # #Leftleg
        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso", child = "LeftLeg", type = "revolute", position =[-.5,0,1],jointAxis="0 1 0")
        pyrosim.Send_Cube(name = "LeftLeg", pos=[-.5,0,0],  size=[1,0.2,0.2], color="5 1.0 1.0 1.0", color_name="pink")
        #LeftLowerLeg
        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg", parent="LeftLeg", child = "LeftLowerLeg", type = "revolute", position= [-1,0,0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-.5] , size=[0.2,0.2,1], color="5 1.0 1.0 1.0", color_name="pink")
        #Rightleg
        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso", child = "RightLeg", type = "revolute", position =[.5,0,1],jointAxis="0 1 0")
        pyrosim.Send_Cube(name = "RightLeg", pos=[.5,0,0],  size=[1,0.2,0.2], color="5 1.0 1.0 1.0", color_name="pink")
        #RightLowerLeg
        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg", parent="RightLeg", child = "RightLowerLeg", type = "revolute", position= [1,0,0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-.5] , size=[0.2,0.2,1], color="5 1.0 1.0 1.0", color_name="pink")
        
        pyrosim.End()
        
    
    def Generate_Brain(self):
        #NEURONS
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        #Torso
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        #Upper
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")

        #Lower
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "RightLowerLeg")

        

        
        #Upper
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 11, jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 12, jointName = "Torso_RightLeg")
        #Lower
        pyrosim.Send_Motor_Neuron( name = 13, jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 14, jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 15, jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName = "RightLeg_RightLowerLeg")
        
        # pyrosim.Send_Synapse(sourceNeuronName= 1, targetNeuronName= 1, weight=self.weights[1][1])
        # pyrosim.Send_Synapse(sourceNeuronName= 1, targetNeuronName= 2, weight=self.weights[1][1])
        
        # pyrosim.Send_Synapse(sourceNeuronName= 2, targetNeuronName= 1, weight=self.weights[2][1])
        # pyrosim.Send_Synapse(sourceNeuronName= 2, targetNeuronName= 2, weight=self.weights[2][1])

        # pyrosim.Send_Synapse(sourceNeuronName= currentRow, targetNeuronName= (currentColumn+c.numSensorNeurons), weight=self.weights[currentRow][currentColumn])
        

        
           
        for currentRow in range(0,c.numSensorNeurons):
            for currentColumn in range(0,c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName= currentRow, targetNeuronName= (currentColumn+c.numSensorNeurons), weight=self.weights[currentRow][currentColumn])
        
        pyrosim.End()
        
        

    def Start_Simulation(self, type):
        
        self.Create_World()
        self.three_joint()
        self.Generate_Brain()
        if type == "GUI":
            os.system(f"python simulate.py {type} {str(self.myID)}")
        else:
            os.system(f"START /B python simulate.py {type} {str(self.myID)}")
       

       
    
    def Wait_For_Simulation_To_End(self, type):
        
        while not os.path.exists(f"fitness{str(self.myID)}.txt"):
            time.sleep(0.05)
            print("NOBODY")
        
        time.sleep(0.01)
        
        f = open(f"fitness{str(self.myID)}.txt")
        self.fitness = float(f.read())
        f.close()
        
        f = open("fitnesses.txt", 'a')
        f.write(f"{self.fitness} \n")
        f.close()
        
        os.system(f"del fitness{str(self.myID)}.txt")
    
        
        
    def Evaluate(self, type):
        pass
        
        
        
    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons-1)
        randomCol = random.randint(0,c.numMotorNeurons-1)
        self.weights[randomRow][randomCol] = random.random() * 2 - 1
        
    def Set_ID(self, id):
        self.myID = id
    
        
    
    
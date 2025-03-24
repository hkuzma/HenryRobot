import numpy as np
import pyrosim.pyrosim as pyrosim
import time
import pyrosim.material as material
import random
import os

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
        self.weights = np.random.rand(3,2)
        self.weights = (self.weights *2 - 1)
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[world_x,world_y,world_z] , size=[length,width,height])
        pyrosim.End()
       
    
    def three_joint(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[1,0,1.5] , size=[length,width,height])
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [.5,0,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-.5,0,-.5] , size=[length,width,height], color="1.0 5 0.0 1.0", color_name="green")
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [1.5,0,1])
        
        #Added params to change color of link, will not work with source code for pyrosim!!!
        # color string follows format "0 1.0 1.0 1.0" (rgba)
        pyrosim.Send_Cube(name="FrontLeg", pos=[.5,0,-.5] , size=[length,width,height], color="5 1.0 1.0 1.0", color_name="pink")
        
        pyrosim.End()
        
    
    def Generate_Brain(self):
        #NEURONS
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
           
        for currentRow in range(0,3):
            for currentColumn in range(0,2):
                pyrosim.Send_Synapse(sourceNeuronName= currentRow, targetNeuronName= (currentColumn+3), weight=self.weights[currentRow][currentColumn])
        
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
            time.sleep(0.01)
        
        f = open(f"fitness{str(self.myID)}.txt")
        self.fitness = float(f.read())
        f.close()
        
        os.system(f"del fitness{str(self.myID)}.txt")
    
        
        
    def Evaluate(self, type):
        pass
        
        
        
    def Mutate(self):
        randomRow = random.randint(0,2)
        randomCol = random.randint(0,1)
        self.weights[randomRow][randomCol] = random.random() * 2 - 1
        
    def Set_ID(self, id):
        self.myID = id
    
        
    
    
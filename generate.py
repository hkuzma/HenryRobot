import pyrosim.pyrosim as pyrosim
import time
import pyrosim.material as material

length = 1
width = 1
height = 1

robot_x =0
robot_y = 0
robot_z = 0.5

world_x = -3
world_y = 3
world_z = 0.5

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[world_x,world_y,world_z] , size=[length,width,height])
    pyrosim.End()
    
def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Link0", pos=[robot_x,robot_y,robot_z] , size=[length,width,height])
    #Create Joint to Hold Leg
    pyrosim.Send_Joint( name = "Link0_Link1" , parent= "Link0" , child = "Link1" , type = "revolute", position = [0,0,1])
    pyrosim.Send_Cube(name="Link1", pos=[0,0,.5] , size=[length,width,height])
    pyrosim.Send_Joint( name = "Link1_Link2" , parent= "Link1" , child = "Link2" , type = "revolute", position = [0,0,1])
    pyrosim.Send_Cube(name="Link2", pos=[0,0,.5] , size=[length,width,height])
    pyrosim.Send_Joint( name = "Link2_Link3" , parent= "Link2" , child = "Link3" , type = "revolute", position = [0,1,0])
    pyrosim.Send_Cube(name="Link3", pos=[0,0,.5] , size=[length,width,height])
    pyrosim.Send_Joint( name = "Link3_Link4" , parent= "Link3" , child = "Link4" , type = "revolute", position = [0,1,0])
    pyrosim.Send_Cube(name="Link4", pos=[0,0,.5] , size=[length,width,height])
    pyrosim.Send_Joint( name = "Link4_Link5" , parent= "Link4" , child = "Link5" , type = "revolute", position = [0,0,-1])
    pyrosim.Send_Cube(name="Link5", pos=[0,0,.5] , size=[length,width,height])
    pyrosim.Send_Joint( name = "Link5_Link6" , parent= "Link5" , child = "Link6" , type = "revolute", position = [0,0,-1])
    pyrosim.Send_Cube(name="Link6", pos=[0,0,.5] , size=[length,width,height])
    
    pyrosim.End()
    
def three_joint():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[1,0,1.5] , size=[length,width,height])
    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [.5,0,1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-.5,0,-.5] , size=[length,width,height], color="1.0 5 0.0 1.0", color_name="green")
    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [1.5,0,1])
    
    #Added params to change color of link, will not work with source code for pyrosim!!!
    # color string follows format "0 1.0 1.0 1.0" (rgba)
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5,0,-.5] , size=[length,width,height], color="5 1.0 1.0 1.0", color_name="pink")
    
    pyrosim.End()

    

    

    
    




    
Create_World()
three_joint()
#Create_Robot()



# for j in range(0,5):
#     y = y+1
#     x = -3
#     for k in range(0,5):
#         x = x+1
#         length = 1
#         width = 1
#         height =1
#         for i in range(0,10):
            


#pyrosim.Send_Cube(name="Box2", pos=[x+1,y,z+1] , size=[length,width,height])








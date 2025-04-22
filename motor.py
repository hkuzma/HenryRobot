import numpy
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
    
    def __init__(self, jointName):
        motor = MOTOR
        
        self.jointName = jointName
        # motor.Prepare_To_Act(self)
        
        self.desiredAngle = 0
        
        
        
    # def Prepare_To_Act(self):
        
    #     self.offset = c.phaseOffset
    #     self.amplitude = c.amplitude
    #     #self.frequency = c.amplitude

        
    #     if self.jointName == b"Torso_BackLeg":
    #         self.frequency = c.frequency
    #         print("half speed")  
    #     elif self.jointName == b"Torso_FrontLeg":
    #         self.frequency = (c.frequency) * 2
    #         print("double speed")
            
        
        # self.frontMotorVector = numpy.linspace(c.NUMPY_START, c.NUMPY_STOP, c.RUNTIME)
        # self.motorValues = self.amplitude * numpy.sin(self.frequency * self.frontMotorVector + self.offset)
    
    def Set_Value(self, robot, desiredAngle):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robot.robotId, 
                                    jointName = self.jointName,
                                    controlMode = p.POSITION_CONTROL,
                                    targetPosition = desiredAngle,
                                    maxForce = c.MAXFORCE)
        self.desiredAngle = desiredAngle
    
    def Get_Value(self):
        return self.desiredAngle
        # print(self.frequency)
        
    # def Save_Motor_Values(self):    
    #     numpy.save(f"data\\{self.jointName}motorValues", self.motorValues)
        

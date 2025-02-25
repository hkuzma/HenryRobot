import numpy
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
    
    def __init__(self, jointName):
        motor = MOTOR
        
        self.jointName = jointName
        motor.Prepare_To_Act(self)
        
        
        
        
    def Prepare_To_Act(self):
        
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.offset = c.phaseOffset
        
        self.frontMotorVector = numpy.linspace(c.NUMPY_START, c.NUMPY_STOP, c.RUNTIME)
        self.motorValues = self.amplitude * numpy.sin(self.frequency * self.frontMotorVector + self.offset)
    
    def Set_Value(self, robot, t):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robot.robotId, 
                                        jointName = self.jointName,
                                        controlMode = p.POSITION_CONTROL,
                                        targetPosition = self.motorValues[t],
                                        maxForce = c.MAXFORCE)
        

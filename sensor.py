import constants as c
import numpy 
import pyrosim.pyrosim as pyrosim

class SENSOR:

    
    def __init__(self, linkName):
        sensor = SENSOR
        self.linkName = linkName
        sensor.Prepare_To_Sense(self)
    
    def Prepare_To_Sense(self):
        self.values = numpy.zeros(c.RUNTIME)
    
    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        
    def Get_Values(self):
        return self.values
    
    def saveSensorValues(self):
        numpy.save(f"data\\{self.linkName}SensorValues.npy", self.values)

from simulation import SIMULATION
from pyrosim.neuralNetwork import NEURAL_NETWORK
import sys
import os



try:
    directOrGUI = sys.argv[1]
except:
    directOrGUI = "BOOGLE"
    
try: 
    solutionID = sys.argv[2]
except:
    solutionID = ''

sim = SIMULATION(directOrGUI, solutionID)
sim.run()
sim.Get_Fitness()
sim.__del__()

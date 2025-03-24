from simulation import SIMULATION
from pyrosim.neuralNetwork import NEURAL_NETWORK
import sys



try:
    directOrGUI = sys.argv[1]
except:
    directOrGUI = "BOOGLE"
    
try: 
    solutionID = sys.argv[2]
except:
    solutionID = 2

sim = SIMULATION(directOrGUI, solutionID)
sim.run()
sim.Get_Fitness()
sim.__del__()

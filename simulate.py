from simulation import SIMULATION
from pyrosim.neuralNetwork import NEURAL_NETWORK
import sys



try:
    directOrGUI = sys.argv[1]
except:
    directOrGUI = "BOOGLE"

sim = SIMULATION(directOrGUI)
sim.run()
sim.Get_Fitness()
sim.__del__()

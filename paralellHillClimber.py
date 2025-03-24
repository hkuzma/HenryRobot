from solution import SOLUTION
import constants as c
import copy
import os

class PARALELL_HILL_CLIMBER:
    
    def __init__(self):
        
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")

        
        self.nextAvailableID = 0
        
        self.parents = {}
        for parent in range (c.populationSize):
            self.parents[parent] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID +=1
        

        
        
        
    
    def Evolve(self):
        self.Evaluate(self.parents)
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
                
            
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for parent in self.parents: 
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID +=1
        
    def Mutate(self):
        for child in self.children:
            self.children[child].Mutate()
      
    def Select(self):
        for i in self.parents:
            if(self.children[i].fitness < self.parents[i].fitness):
                self.parents[i] = self.children[i]
    
        
    def Print(self):
        print("==============================================================================")
        for i in self.parents:
            print(f"\n\nPARENT : {self.parents[i].fitness} , CHILD : {self.children[i].fitness}\n\n")
        
        print("==============================================================================")

    def Show_Best(self):
        lowest = 5
        index = -1
        for parent in self.parents:
            if self.parents[parent].fitness<lowest:
                lowest = self.parents[parent].fitness
                index = parent        

        print(index)    
            
        self.parents[index].Start_Simulation("GUI")
    
    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")
        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End("DIRECT")
        

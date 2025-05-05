from solution import SOLUTION
import constants as c
import copy
import os
import time
import math

class PARALELL_HILL_CLIMBER:
    
    def __init__(self):
        
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        os.system("del tmp*.txt")


        
        self.nextAvailableID = 0
        
        self.parents = {}
        for parent in range (c.populationSize):
            self.parents[parent] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID +=1
        

        
        
        
    
    def Evolve(self):
        self.Evaluate(self.parents)
        num = 0
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(num)
            num +=1
            
    def write_fitness(self, gen):
        g = open("Generational BEST Fitness.txt", "a")
        f = open("Generational Fitness.txt", "a")
        fitnesses = open("A.txt", 'a')
        
        if gen == 0:
            f.write("\nNEW RUN\n")
            fitnesses.write("\nNEW RUN\n")
            g.write("\nNEW RUN\n")
            
        lowest = -1000
        index = -1
        for parent in self.parents:
            if self.parents[parent].fitness>lowest:
                lowest = self.parents[parent].fitness
                index = parent        

            
        g.write(f"Generation {gen} : {self.parents[index].fitness}\n")
        g.close()

        
        generationFitness = 0
        numParents = 0
        for parent in self.parents:
            generationFitness += self.parents[parent].fitness
            fitnesses.write(f"{self.parents[parent].fitness} \n")
            numParents +=1
        
        avgGenerationFitness = generationFitness/numParents
            
        f.write(f"Generation {gen}: {avgGenerationFitness}\n")
        f.close()
        fitnesses.close()
                
            
    def Evolve_For_One_Generation(self, gen):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.write_fitness(gen)

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
            if(self.children[i].fitness > self.parents[i].fitness):
                self.parents[i] = self.children[i]
    
        
    def Print(self):
        print("==============================================================================")
        for i in self.parents:
            print(f"\n\nPARENT : {self.parents[i].fitness} , CHILD : {self.children[i].fitness}\n\n")
        
        print("==============================================================================")

    def Show_Best(self):
        lowest = -1000000000000000000000000000000000000000000000000000000000000
        index = 0
        for parent in self.parents:
            if self.parents[parent].fitness>lowest:
                lowest = self.parents[parent].fitness
                index = parent        

        print(index)    
            
        self.parents[index].Start_Simulation("GUI")
    
    def Evaluate(self, solutions):
        halfway_index = 0
        for i in range(0,math.floor(len(solutions)/2)):
            solutions[i].Start_Simulation("DIRECT")
            halfway_index +=1
        for i in range(0,math.floor(len(solutions)/2)):
            solutions[i].Wait_For_Simulation_To_End("DIRECT")
            #time.sleep(.01)
        for i in range(halfway_index,len(solutions)):
            solutions[i].Start_Simulation("DIRECT")

        
        for i in range(halfway_index,len(solutions)):
            solutions[i].Wait_For_Simulation_To_End("DIRECT")


        

import pybullet as p

class WORLD:
    
    def __init__(self):
        
        world = WORLD
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("world.sdf")


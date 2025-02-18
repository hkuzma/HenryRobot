from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, color, color_name): #Henry added params for color and color_name

        self.depth  = 3


        if color_name == "cyan" and color == "0 1.0 1.0 1.0":
        

            self.string1 = '<material name="Cyan">'

            self.string2 = '    <color rgba="0 1.0 1.0 1.0"/>'

        #Henry IMPLEMENTATION FOR ALT COLOR
        else:
            self.string1 = f'<material name="{color_name}">'
        
            self.string2 = f'    <color rgba="{color}"/>'
        #======================================================
            
            
        self.string3 = '</material>'

    # def alt(self, color, color_name):
        
    #     self.depth = 3
        
    #     self.string1 = f'<material name = "{color_name}">'
        
    #     self.string2 = f'    <color rgba="{color}"/>'
        
    #     self.string3 = '</material>'
        
    #     return self
        

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
        
    def setColor(color, self):
        self.string2 = f'    <color rgba={color}/>'



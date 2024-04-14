class object_base:
    def __init__(self, image):
        self.m = 0 #mass
        self.p = 0 #pos
        self.v = 0 #vel
        self.image = image
        
    @property
    def mass(self):
        return self.m
    @property
    def vel(self):
        return self.v
    @property
    def pos(self):
        return self.p
    
    def draw(self):
        pass

    def update(self):
        pass

    def destroy(self):
        pass



class sattelite_base(object_base):
    def __init__(self): #, mass, pos, vel):
        super().__init__("blue.png")
        
class rock_base(object_base):
    def __init__(self): #, mass, pos, vel):
        super().__init__("red.png")
class Activity:
    def __init__(self,capacity,name):
        self.capacity = capacity
        self.name = name
    def __repr__(self):
        return self.name + ' ::: ' +'capacity: ' + str(self.capacity) 

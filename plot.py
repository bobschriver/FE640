class Plot:
    def __init__(self, number, volume):
        self.number = number
        self.volume = volume
    
    def __str__(self):
        return '{}'.format(self.number)
    
    def __repr__(self):
        return str(self)
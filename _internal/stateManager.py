from settings import *

class GameStateManager:
    def __init__(self, currentState = "Options"):
        self.currState = currentState
        self.taking = False
        
    def getState(self):
        return self.currState
    
    def setState(self, state):
        self.currState = state
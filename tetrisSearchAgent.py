import tetris
from tetris import TetrisApp
import util
import time
import TetrisSearch

class SearchAgent(Agent):

    #Get the search function from its name
    def __init__(self, fn = "breadthFirstSearch"):
        if fn not in dir(TetrisSearch):
            raise AttributeError, fn + " is not in TetrisSearch.py."
        func = getattr(TetrisSearch, fn)


    def registerInitialState(self, state):
        """
        Agent sees layout of game for first time
        Compute path to goal and store in local variable
        state = a GameState object (TetrisSearch.py)
        """
        if self.searchFunction == None: raise Exception, "No search function provided for SearchAgent"
        startTime = time.time()
        problem = self.searchType(state)
        self.actions = self.searchFunction(problem)
        print("Path found in %.1f seconds" % (time.time() - startTime))

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState). Returns gameover if no more actions to take.
        state = a GameState object (TetrisSearch.py)

        """
        self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            self.gameover = True
            return self.gameover

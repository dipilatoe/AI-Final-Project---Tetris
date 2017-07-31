import pygame, sys
import tetris
from tetris import TetrisApp
import time
import TetrisSearch

class SearchAgent():

    #Get the search function from its name
    def __init__(self, fn = "breadthFirstSearch"):
        if fn not in dir(TetrisSearch):
            raise AttributeError, fn + " is not in TetrisSearch.py."
        func = getattr(TetrisSearch, fn)
        self.searchFunction = func

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
        dont_burn_my_cpu = pygame.time.Clock()
        key_actions = {
            'ESCAPE':	state.quit,
            'LEFT':		lambda:state.move(-1),
            'RIGHT':	lambda:state.move(+1),
            'DOWN':		lambda:state.drop(True),
            'UP':		state.rotate_stone,
            'p':		state.toggle_pause,
            'SPACE':	state.start_game,
            'RETURN':	state.insta_drop
        }

        self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        for event in pygame.eveng.get():
            if event.type == pygame.USEREVENT+1:
                self.drop(False)
            elif event.type == pygame.QUIT:
                self.quit()
            elif i < len(self.actions):
                for key in key_actions:
                    if self.actions[i] == eval(key):
                        return key_actions[key]()
                if event.type == pygame.USEREVENT+1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
        else:
            return TetrisApp.quit()

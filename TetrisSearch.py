from random import randint
import tetris
from tetris import TetrisApp

class RandomAgent():
    def getAction(self, gameState):
        actionList = state.getActions(TetrisApp.stone)
        return actionList[randint(0,len(actionList))]


class ExpectimaxAgent():
   
     
    def getAction(self, gameState):
     
        return self.value(gameState, self.depth-1, tetris.TetrisApp.stone)
    def value(self, state, depthLimit, currentDepth, currentPiece):
        

		#get successor states if not terminal
        if(currentPiece is not 0):
            if(tetris.TetrisApp.isGameOver(state,currentPiece)):
                return -9999999
            successorList = list()
            actionList = state.getActions(currentPiece)
        #get averages with each on the shape list
        else:
            avg = 0.0
            for x in tetris.tetris_shapes:
                avg = avg + value(state, depthLimit, currentDepth, x)
            return avg/len(tetris.tetris_shapes)

		#return action at top of tree
        if(currentDepth==0):
<<<<<<< HEAD
            scoreHold, action = max([(self.value(state.generateSuccessor(tetris.TetrisApp.stone, x), depthLimit,1, tetris.TetrisApp.next_stone),x) for x in actionList])
=======
            scoreHold, action = max([(self.value(state.generateSuccessor(TetrisApp.stone, x), depthLimit,1, 1),x) for x in actionList])
>>>>>>> c4af175cc591c0c87b330b2f56e458935d81c216
            return action
        #for previewed piece
	    if(currentDepth==1):
            return max(self.value(state.generateSuccessor(TetrisApp.next_stone, x), depthLimit, 2, 0 )for x in actionList)

		#return score at max depth
        if(currentDepth==depthLimit and currentPiece is not 0):
            return min(scoreEvaluationFunction(state.generateSuccessor(currentPiece,x) for x in actionList)

	    #all other cases (standard)
        return max(self.value(state.generatesuccessor(currentPiece,x) depthLimit, currentDepth+1, 0) for x in actionList)
    def evaluationFunction(state):
        return state.getScore() * (1/len(getPieces.asList())
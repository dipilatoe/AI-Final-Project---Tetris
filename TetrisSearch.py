from random import randint
import tetris
from tetris import TetrisApp

class RandomAgent():
    #generates list of final positions
    def getActions():
        positions = []
        for x in range(10)
            positions.append(tetris.join_matrices(board, TetrisApp.stone, (x,0)), x, 0)
            for y in range(22)
                if not check_collision(board, TetrisApp.stone, (x,y))
                    position = positions[x]
                    if y > position[2]
                        positions.pop()
                        positions.append(tetris.join_matrices(board, TetrisApp.stone, (x,y)), x, y)
        
        return positions
    #chooses randomly a final position from a list of all available final positions
    def getAction(self, gameState):
        actionList = state.getActions(TetrisApp.stone)
        return actionList[randint(0,len(actionList))]

class ExpectimaxAgent():
    
    def getAction(self, gameState):
     
        return self.value(gameState, self.depth-1, 1)
    def value(self, state, depthLimit, currentDepth, currentPiece):
        if(state.isGameOver()):
            return self.evaluationFunction(state)

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
            scoreHold, action = max([(self.value(state.generateSuccessor(TetrisApp.stone, x), depthLimit,1, 1),x) for x in actionList])
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
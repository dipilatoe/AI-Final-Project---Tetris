from random import randint
import tetris
from tetris import TetrisApp

#returns the base coordinate for the stone, the current state of the game board, and the next stone
def getGameState():
    return TetrisApp.stone_x, TetrisApp.stone_y, board, TetrisApp.next_stone, TetrisApp.score, TetrisApp.stone

#generates a list of successors of potential states where the stone has moved left/right or rotated
#CHANGE TO USE GAMESTATE INSTEAD OF DIRECTLY REFERENCING VARIABLES IN TETRIS.PY
#def generateSuccessor(self, gameState, stone, action):
#    successors = []
#    if not tetris.check_collision(board, TetrisApp.stone, (TetrisApp.stone_x - 1, TetrisApp.stone_y)):
#        successors.append(tetris.join_matrixes(board, TetrisApp.stone, (TetrisApp.stone_x-1, TetrisApp.stone_y)))
#    if not tetris.check_collision(board, TetrisApp.stone, (TetrisApp.stone_x + 1, TetrisApp.stone_y)):
#        successors.append(tetris.join_matrixes(board, TetrisApp.stone, (TetrisApp.stone_x+1, TetrisApp.stone_y)))
#    TetrisApp.rotate_stone
#    successors.append(tetris.join_matrixes(board, TetrisApp.stone, (TetrisApp.stone_x, TetrisApp.stone_y)))
#    return successors

#generates list of final positions (RETURN LIST OF TUPLES - CONTAINS PIECE'S FINAL X POSITION, FINAL Y POSITION, SHAPE)
def finalPositions(self, board, piece):
    positions = []
    #if shape is square, loop through finding final positions just once, don't care about rotations
    if piece == tetris_shapes[6]:
        for x in range(10):
            positions.append(x, 0, piece)
            for y in range(22):
                if not check_collision(board, piece, (x,y)):
                    position = positions[x]
                    if y > position[1]:
                        positions.pop()
                        positions.append(x, y, piece)
    #if shape is line, Z or S, loop through twice to take into account a rotation of the piece
    if piece == tetris_shapes[5] or piece == tetris_shapes[1] or piece == tetris_shapes[2]:
        for z in range(2):
            for x in range(10):
                positions.append(x, 0, piece)
                for y in range(22):
                    if not check_collision(board, piece, (x,y)):
                        position = positions[x]
                        if y > position[1]:
                            positions.pop()
                            positions.append(x, y, piece)
            piece = tetris.rotate_clockwise(piece)
    #all other pieces (L/J/T shapes) run four times to take into account the 3 rotations
    else:
        for z in range(4):
            for x in range(10):
                positions.append(x, 0, piece)
                for y in range(22):
                    if not check_collision(board, piece, (x,y)):
                        position = positions[x]
                        if y > position[1]:
                            positions.pop()
                            positions.append(x, y, piece)
            piece = tetris.rotate_clockwise(piece)
    
    return positions

class RandomAgent():
    #chooses randomly a final position from a list of all available final positions
    def getAction(self, gameState):
        actionList = state.finalPositions(TetrisApp.stone)
        return actionList[randint(0,len(actionList))]

class ExpectimaxAgent():
    
    def getAction(self, gameState):
     
        return self.value(gameState[2], 3, 0, gameState[5])
    def value(self, board, depthLimit, currentDepth, currentPiece):

		#get successor states if not terminal, returns low negative number if it is terminal.
        if(currentPiece is not 0):
            if(tetris.TetrisApp.isGameOver(board,currentPiece)):
                return -9999999
            successorList = list()
            actionList = state.finalPositions(board, currentPiece)
        #if no shape is set, generate list of shapes and get expected value (average) of best move with each shape
        else:
            avg = 0.0
            for x in tetris.tetris_shapes:
                avg = avg + value(board, depthLimit, currentDepth, x)
            return avg/len(tetris.tetris_shapes)

		#return action at top of tree
        if(currentDepth==0):
            scoreHold, action = max([(self.value(tetris.join_matrixes(board,x[2], (x[0],x[1])), depthLimit,1, 1),x) for x in actionList])
            return action
        #for previewed piece
	    if(currentDepth==1):
            return max(self.value((tetris.join_matrixes(board,x[2], (x[0],x[1])), depthLimit, 2, 0 )for x in actionList)

		#return score at max depth
        if(currentDepth==depthLimit and currentPiece is not 0):
            return min(scoreEvaluationFunction(tetris.join_matrixes(board,x[2], (x[0],x[1])) for x in actionList)

	    #all other cases (standard)
        return max(self.value(tetris.join_matrixes(board,x[2], (x[0],x[1])), depthLimit, currentDepth+1, 0) for x in actionList)
    def evaluationFunction(board):
        return board[4] * (1/len(getPieces.asList())
		#^Need to change this to count filled pieces, not yet implemented.
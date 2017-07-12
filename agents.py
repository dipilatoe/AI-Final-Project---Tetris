import tetris
from tetris import TetrisApp

class Agents

    #returns the base coordinate for the stone, the current state of the game board, and the next stone
    def getGameState():
        return TetrisApp.stone_x, TetrisApp.stone_y, board, TetrisApp.next_stone
    
    #generates a list of successors of potential states where the stone has moved left/right or rotated
    def generateSuccessor():
        successors = []
        if not tetris.check_collision(board, TetrisApp.stone, (TetrisApp.stone_x - 1, TetrisApp.stone_y)):
            successors.append(tetris.join_matrices(board, TetrisApp.stone, (TetrisApp.stone_x-1, TetrisApp.stone_y)))
        if not tetris.check_collision(board, TetrisApp.stone, (TetrisApp.stone_x + 1, TetrisApp.stone_y)):
            successors.append(tetris.join_matrices(board, TetrisApp.stone, (TetrisApp.stone_x+1, TetrisApp.stone_y)))
        TetrisApp.rotate_stone
        successors.append(tetris.join_matrices(board, TetrisApp.stone, (TetrisApp.stone_x, TetrisApp.stone_y)))
        return successors
    
    def randomAgent():
        util.raiseNotDefined()
        
    def greedyAgent():
        util.raiseNotDefined()
        
    def optimalAgent():
        util.raiseNotDefined()
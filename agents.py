import tetris
from tetris import TetrisApp

class Agents

    def getGameState(): #ED
        return TetrisApp.stone_x, TetrisApp.stone_y, board, TetrisApp.next_stone
    
    def getSuccessors():    #ED
        successors = []
        if not tetris.check_collision(board, TetrisApp.stone, (TetrisApp.stone_x - 1, TetrisApp.stone_y)):
            successors.append(tetris.join_matrices(TetrisApp.board, TetrisApp.stone, (TetrisApp.stone_x-1, TetrisApp.stone_y)))
        if not tetris.check_collision(board, TetrisApp.stone, (TetrisApp.stone_x + 1, TetrisApp.stone_y)):
            successors.append(tetris.join_matrices(TetrisApp.board, TetrisApp.stone, (TetrisApp.stone_x+1, TetrisApp.stone_y)))
        #add in rotation successor
        return successors
    
    def randomAgent():
        util.raiseNotDefined()
        
    def greedyAgent():
        util.raiseNotDefined()
        
    def optimalAgent():
        util.raiseNotDefined()
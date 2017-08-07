#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# NOTE FOR WINDOWS USERS:
# You can download a "exefied" version of this game at:
# http://hi-im.laria.me/progs/tetris_py_exefied.zip
# If a DLL is missing or something like this, write an E-Mail (me@laria.me)
# or leave a comment on this gist.

# Very simple tetris implementation
#
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!

# Copyright (c) 2010 "Laria Carolin Chabowski"<me@laria.me>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from random import randint
from random import randrange as rand
import pygame, sys

# The configuration
cell_size = 18
cols =      10
rows =      22
maxfps =    30

colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35) # Helper color for background grid
]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

def rotate_clockwise(shape):
    return [ [ shape[y][x] for y in xrange(len(shape)) ] for x in xrange(len(shape[0]) - 1, -1, -1) ]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]
    return [[0 for i in xrange(cols)]] + board

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1 ][cx+off_x] += val
    return mat1

def new_board():
    board = [ [ 0 for x in xrange(cols) ] for y in xrange(rows) ]
    board += [[ 1 for x in xrange(cols)]]
    return board

#WIP method to replace our use of join_matrixes
def newBoard(board, x, y, stone, newX, newY):
    for yB in range(y, y+len(stone)):
        for xB in range(x, x+len(stone[0])):
            if stone[yB-y][xB-x] != 0:
                board[yB][xB] = 0
    for yB in range(y, y+len(stone)):
        for xB in range(x, x+len(stone[0])):
            if stone[yB-y][xB-x] != 0:
                board[yB + newY][xB + newX] = 1
    return board

#generates list of final positions (RETURN LIST OF TUPLES - CONTAINS PIECE'S FINAL X POSITION, FINAL Y POSITION, SHAPE)
def finalPositions(board, piece):
    positions = []
    #if shape is square, loop through finding final positions just once, don't care about rotations
    if piece == tetris_shapes[6]:
        for x in range(10):
            positions.append((x, 0, piece))
            for y in range(22):
                if not check_collision(board, piece, (x,y)):
                    position = positions[x]
                    if y > position[1]:
                        positions.pop()
                        positions.append((x, y, piece))
    #if shape is line, Z or S, loop through twice to take into account a rotation of the piece
    elif piece == tetris_shapes[5] or piece == tetris_shapes[1] or piece == tetris_shapes[2]:
        for z in range(2):
            for x in range(10):
                positions.append((x, 0, piece))
                for y in range(22):
                    if not check_collision(board, piece, (x,y)):
                        position = positions[x]
                        if y > position[1]:
                            positions.pop()
                            positions.append((x, y, piece))
            piece = rotate_clockwise(piece)
    #all other pieces (L/J/T shapes) run four times to take into account the 3 rotations
    elif piece == tetris_shapes[0] or piece == tetris_shapes[3] or piece == tetris_shapes[4]:
        for z in range(4):
            for x in range(10):
                positions.append((x, 0, piece))
                for y in range(22):
                    if not check_collision(board, piece, (x,y)):
                        position = positions[x]
                        if y > position[1]:
                            positions.pop()
                            positions.append((x, y, piece))
            piece = rotate_clockwise(piece)

    return positions

class RandomAgent():
    @staticmethod
    #chooses randomly a final position from a list of all available final positions
    def getAction(gameState):
        actionList = finalPositions(gameState[2], gameState[5])
        print actionList
        return actionList[randint(0,len(actionList)-1)]

class ExpectimaxAgent():

    def getAction(self, gameState):

        return self.value(gameState[2], 3, 0, gameState[5])
    def value(self, board, depthLimit, currentDepth, currentPiece):

        #get successor states if not terminal, returns low negative number if it is terminal.
        if(currentPiece is not 0):
            if(TetrisApp.isGameOver(board,currentPiece)):
                return -9999999
            successorList = list()
            actionList = finalPositions(board, currentPiece)
        #if no shape is set, generate list of shapes and get expected value (average) of best move with each shape
        else:
            avg = 0.0
            for x in tetris.tetris_shapes:
                avg = avg + value(board, depthLimit, currentDepth, x)
            return avg/len(tetris_shapes)

        #return action at top of tree
        if(currentDepth==0):
            scoreHold, action = max([(self.value(join_matrixes(board,x[2], (x[0],x[1])), depthLimit,1, 1),x) for x in actionList])
            return action
        #for previewed piece
        if(currentDepth==1):
            return max(self.value((join_matrixes(board,x[2], (x[0],x[1])), depthLimit, 2, 0 )for x in actionList))

        #return score at max depth
        if(currentDepth==depthLimit and currentPiece is not 0):
            return min(evaluationFunction(join_matrixes(board,x[2], (x[0],x[1])) for x in actionList))

        #all other cases (standard)
        return max(self.value(join_matrixes(board,x[2], (x[0],x[1])), depthLimit, currentDepth+1, 0) for x in actionList)

    def evaluationFunction(board):
        return board[4] * (1/len(getPieces.asList()))

class GreedyAgent():
    def getAction(self, GameState):
        actionList = GameState.finalPositions(board, GameState[5])
        scoreHold, action = max([(evaluationFunction(tetris.join_matrixes(board,x[2], (x[0],x[1]))),x) for x in actionList])
        return action

    def evaluationFunction(board):
        return board[4] * (1/len(getPieces.asList()))

class SolutionSearch():
    @classmethod
    def isGoalState(self, currentState, goalState):
        return (currentState[0] == goalState[0] and currentState[1] == goalState[1])
    #generates a list of successors of potential states where the stone has moved left/right or rotated
    #state[2] = board
    #state[5] = stone
    #state[0] = stone x coordinate
    #state[1] = stone y coordinate
    @classmethod
    def getSuccessors(self, state):
        successors = []
        #moving left/right
        if not check_collision(state[2], state[5], (state[0] - 1, state[1])):
            successors.append(((state[0] - 1), state[1], newBoard(state[2], state[0], state[1], state[5], state[0] - 1, state[1]), state[3], state[4], state[5], 'LEFT'))
        #moving right
        if not check_collision(state[2], state[5], (state[0] + 1, state[1])):
            successors.append(((state[0] + 1), state[1], newBoard(state[2], state[0], state[1], state[5], state[0] + 1, state[1]), state[3], state[4], state[5], 'RIGHT'))
        #rotate stone
        if not check_collision(state[2], rotate_clockwise(state[5]), (state[0], state[1])):
            successors.append((state[0], state[1], newBoard(state[2], state[0], state[1], rotate_clockwise(state[5]), state[0], state[1]), state[3], state[4], rotate_clockwise(state[5]), 'UP'))
        #drop down one line
        if not check_collision(state[2], state[5], (state[0], state[1] + 1)):
            successors.append((state[0], state[1] + 1, newBoard(state[2], state[0], state[1], state[5], state[0], state[1] + 1)))
        return successors
    @classmethod
    def graphSearch(self, initialState, goalState, frontier):
        explored = []    #list of nodes that have been explored
        frontier.push((initialState, []))   #creates the frontier
        while not frontier.isEmpty(): #continues until the frontier is empty, at the end just returns an empty set in absense of a solution
            state, actions = frontier.pop() #removes from the frontier the current node to be expanded
            if not state in explored: #if that node is not in explored then we expand it and also add it to explored
                explored.append(state)
                if self.isGoalState(state, goalState): #goal state check
                    return actions
                successors = self.getSuccessors(state) #expanding the node
                for successor in successors:    #adding each expansion into the frontier
                    newActions = actions + [successor[6]]
                    frontier.push((successor, newActions))
        return []

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in xrange(cols)] for y in xrange(rows)]

        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 12)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) # We do not need
                                                     # mouse movement
                                                     # events, so we
                                                     # block them.
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True
    #Added gameover method for optimal agent/evaluation function
    def isGameOver(self,board1, stone1):
        return check_collision(board1,stone1,(int(cols / 2 - len(stone1[0])/2), 0))

    def init_game(self):
        self.board = new_board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    #returns the base coordinate for the stone, the current state of the game board, and the next stone
    def getGameState(self):
        return self.stone_x, self.stone_y, self.board, self.next_stone, self.score, self.stone

    def disp_msg(self, msg, topleft):
        x,y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
              self.width // 2-msgim_center_x,
              self.height // 2-msgim_center_y+i*22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, colors[val],
                        pygame.Rect((off_x+x) * cell_size, (off_y+y) * cell_size, cell_size, cell_size),0)

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x
    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def run(self):
        key_actions = {
            'ESCAPE':   self.quit,
            'LEFT':     lambda:self.move(-1),
            'RIGHT':    lambda:self.move(+1),
            'DOWN':     lambda:self.drop(True),
            'UP':       self.rotate_stone,
            'p':        self.toggle_pause,
            'SPACE':    self.start_game,
            'RETURN':   self.insta_drop
        }
        
        self.gameover = False
        self.paused = False

        dont_burn_my_cpu = pygame.time.Clock()
        
        while 1:
            self.screen.fill((0,0,0))
            if self.gameover:
                self.center_msg("""Game Over!\nYour score: %d\nPress space to continue""" % self.score)
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    pygame.draw.line(self.screen, (255,255,255), (self.rlim+1, 0), (self.rlim+1, self.height-1))
                    self.disp_msg("Next:", (self.rlim+cell_size, 2))
                    self.disp_msg("Score: %d\n\nLevel: %d\nLines: %d" % (self.score, self.level, self.lines), (self.rlim+cell_size, cell_size*5))
                    self.draw_matrix(self.bground_grid, (0,0))
                    self.draw_matrix(self.board, (0,0))
                    self.draw_matrix(self.stone, (self.stone_x, self.stone_y))
                    self.draw_matrix(self.next_stone, (cols+1,2))
            pygame.display.update()

            state = self.getGameState()
            #this line below runs the Random Agent
            actions = SolutionSearch.graphSearch(state, RandomAgent.getAction(state), Queue())
            #this line below runs the Optimal Agent
            actions = SolutionSearch.graphSearch(state, ExpectimaxAgent.getAction(state), Queue())
            #this line below runs the Greedy Agent
            actions = SolutionSearch.graphSearch(state, GreedyAgent.getAction(state), Queue())

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"+key):
                            key_actions[key]()
                
            dont_burn_my_cpu.tick(maxfps)

if __name__ == '__main__':
    App = TetrisApp()
    App.run()

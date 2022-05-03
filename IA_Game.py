import random
import copy 

###############################################################################

request = {'request': 'play', 'lives': 3, 'errors': [], 'state': {'players': ['Co', 'Coco'], 'current': 0, 'board': [[28, 35], [27, 
36]]}}

board = [
      0,  1,  2,  3,  4,  5,  6,  7,
      8,  9, 10, 11, 12, 13, 14, 15,
     16, 17, 18, 19, 20, 21, 22, 23,
     24, 25, 26, 27, 28, 29, 30, 31,
     32, 33, 34, 35, 36, 37, 38, 39,
     40, 41, 42, 43, 44, 45, 46, 47,
     48, 49, 50, 51, 52, 53, 54, 55,
     56, 57, 58, 59, 60, 61, 62, 63
]

weight = [
    120, -20,  20,   5,   5,  20, -20, 120,
    -20, -40,  -5,  -5,  -5,  -5, -40, -20,
    20,  -5,   15,   3,   3,  15,  -5,  20,
    5,   -5,   3,    3,   3,   3,  -5,   5,
    5,   -5,   3,    3,   3,   3,  -5,   5,
    20,  -5,   15,   3,   3,  15,  -5,  20,
    -20, -40,  -5,  -5,  -5,  -5, -40, -20,
    120, -20,  20,   5,   5,  20, -20, 120
]

directions = [
    ( 0,  1),
    ( 0, -1),
    ( 1,  0),
    (-1,  0),
    ( 1,  1),
    (-1,  1),
    ( 1, -1),
    (-1, -1)
]

#############################################################################

def PlayerColor(state):
    color = None
    if state['current']== 0:
        color = 'black'
    elif state['current']== 1:
        color = 'white'
    else:
        return ValueError 
    return color

def PlayersTiles(state,color) :
    opponent = None
    me = None
    if color == 'black':
        me = state['board'][0]
        opponent = state['board'][1]
    elif color == 'white':
        me = state['board'][1]
        opponent = state['board'][0]
    else:
        return TypeError
    return me,opponent

#########################game.py###########################

class GameEnd(Exception):
	def __init__(self, lastState):
		self.__state = lastState

	@property
	def state(self):
		return self.__state

	def __str__(self):
		return 'Game Over'

class GameWin(GameEnd):
	def __init__(self, winner, lastState):
		super().__init__(lastState)
		self.__winner = winner

	@property
	def winner(self):
		return self.__winner

	def __str__(self):
		return super().__str__() + ': {} win the game'.format(self.winner)

class BadMove(Exception):
	pass

class GameDraw(GameEnd):
	def __init__(self, lastState):
		super().__init__(lastState)

	def __str__(self):
		return super().__str__() + ': Draw'

class GameLoop(GameDraw):
	def __init__(self, lastState):
		super().__init__(lastState)

	def __str__(self):
		return super().__str__() + ': Stopped because of lopping behavior'

class BadGameInit(Exception):
	pass

#######################################################################################

from unittest import removeResult

def add(p1, p2):
    l1, c1 = p1
    l2, c2 = p2
    return l1 + l2, c1 + c2

def coord(index):
    return index // 8, index % 8

def index(coord):
    l, c = coord
    return l*8+c

def isInside(coord):
    l, c = coord
    return 0 <= l < 8 and 0 <= c < 8

def walk(start, direction):
    current = start
    while isInside(current):
        current = add(current, direction)
        yield current

def isGameOver(state):
    playerIndex = state['current']
    otherIndex = (playerIndex+1)%2

    res = False
    if len(possibleMoves(state)) == 0:
        state['current'] = otherIndex
        if  len(possibleMoves(state)) == 0:
            res = True
    state['current'] = playerIndex
    return res

def willBeTaken(state, move):
    playerIndex = state['current']
    otherIndex = (playerIndex+1)%2

    if not (0 <= move < 64):
        raise BadMove('Your must be between 0 inclusive and 64 exclusive')

    if move in state['board'][0] + state['board'][1]:
        raise BadMove('This case is not free')

    board = []
    for i in range(2):
        board.append(set((coord(index) for index in state['board'][i])))

    move = coord(move)

    cases = set()
    for direction in directions:
        mayBe = set()
        for case in walk(move, direction):
            if case in board[otherIndex]:
                mayBe.add(case)
            elif case in board[playerIndex]:
                cases |= mayBe
                break
            else:
                break

    if len(cases) == 0:
        raise BadMove('Your move must take opponent\'s pieces')
    
    return [index(case) for case in cases]

def possibleMoves(state):
    res = []
    for move in range(64):
        try:
            willBeTaken(state, move)
            res.append(move)
        except BadMove:
            pass
    return res

def next(state):
    res = possibleMoves(state)
    move = random.choice(res)
    return move

#if __name__ == "__main__":
print(PlayerColor(request['state']))
print(PlayersTiles(request['state'], PlayerColor(request['state'])))

print(possibleMoves(request['state']))

print(next(request['state']))
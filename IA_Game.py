import random
import copy 
from unittest import removeResult
###############################################################################

request = {'request': 'play',
 'lives': 3,
 'errors': [],
 'state': {
      'players': ['Co', 'stupid'],
      'current': 0,
      'board': [
            [28, 36, 35, 43, 19, 51, 33, 42, 11, 25, 18, 52, 44, 45, 10, 50, 53, 26, 17, 55, 37, 46, 7, 15, 23, 31, 39, 47],
            [5, 3, 4, 2, 29, 61, 58, 59, 60, 30, 21, 12, 38, 0, 1, 56, 57, 63, 62, 22, 48, 32, 40, 8, 16, 24, 6, 20, 27, 13, 41, 34]
        ]
    }
}

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

pos_weight = [
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
#############################################################################

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

def ApplyMove(state, move):
    newState = copy.deepcopy(state)
    playerIndex = state['current']
    otherIndex = (playerIndex+1)%2

    if len(possibleMoves(state)) > 0 and move is None:
        raise BadMove('You cannot pass your turn if there are possible moves')

    if move is not None:
        cases = willBeTaken(state, move)

        newState['board'][playerIndex].append(move)

        for case in cases:
            newState['board'][otherIndex].remove(case)
            newState['board'][playerIndex].append(case)
            
    newState['current'] = otherIndex

    #if isGameOver(newState):
    #    if len(newState['board'][playerIndex]) > len(newState['board'][otherIndex]):
    #        winner = playerIndex
    #    elif len(newState['board'][playerIndex]) < len(newState['board'][otherIndex]):
    #            winner = otherIndex
    #    else:
    #        raise GameDraw(newState)
    #    raise GameWin(winner, newState)
        
    return newState

#################################################################################
#################################################################################

def PlayerColor(state):
    color = None
    if state['current']== 0:
        color = 'black'
    elif state['current']== 1:
        color = 'white'
    else:
        return ValueError 
    return color

def OpponentColor(state):
    if state['current']== 0:
        return 'white'
    if state['current']== 1:
        return 'black'
    else:
        return ValueError

def PlayersTiles(state) :
    color = PlayerColor(state)
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
    return me, opponent

def MoveValue(state):
    move = possibleMoves(state)
    value = []
    for elem in move:
        value.append(pos_weight[elem])
    return value

def GetMax(state):
    value = MoveValue(state)
    if len(value) == 0:
        return None
    return max(value)

def FindMax(state):
    maxvalue = GetMax(state)
    value = MoveValue(state)
    move = possibleMoves(state)
    res = []
    s=0
    if GetMax(state) == None:
        return None
    for elem in value:
        if elem == maxvalue:
            res.append(move[s])
        s +=1
    return res

def winner(state):
    me ,opponent = PlayersTiles(state)
    if len(me) > len(opponent):
        return state['current']
    elif len(me) < len(opponent):
        if state['current'] == 0:
            return 1
        elif state['current'] ==1:
            return 0
    else:
        return None

def heuristic(state):
    player = state["current"]
    me ,opponent = PlayersTiles(state)
    if isGameOver(state):
        theWinner = winner(state)
        if theWinner == player:
            return 100
        return -100
    res = len(me) - len(opponent)
    return res

def NegamaxWithPruningLimitedDepth(state, depth=3, alpha=float('-inf'), beta=float('+inf')):
    if isGameOver(state) or depth==0:
        return -heuristic(state), None
    theValue, theMove = float('-inf'), None
    if FindMax(state) == None:
        return -theValue, None
    for move in FindMax(state):
        mov = move
        newState = ApplyMove(state, mov)
        value, _ = NegamaxWithPruningLimitedDepth(newState, depth-1, -beta, -alpha)
        if value > theValue:
            theValue, theMove = value, mov
        alpha = max(alpha, theValue)
        if alpha >= beta:
            break
    return -theValue, theMove

#def next(state):
#    res = FindMax(state)
#    move = random.choice(res)
#    return move

def next(state):
    _, move = NegamaxWithPruningLimitedDepth(state)
    return move



if __name__ == "__main__":
   #print(PlayerColor(request['state']))
   #print(OpponentColor(request['state']))
   #print(PlayersTiles(request['state']))
   #print(winner(request['state']))
   
   #print(possibleMoves(request['state']))
   #print(MoveValue(request['state']))
   #print(GetMax(request['state']))
   #print(FindMax(request['state']))

   print(next(request['state']))
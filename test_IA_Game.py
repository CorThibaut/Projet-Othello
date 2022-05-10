import IA_Game

request = {'request': 'play', 'lives': 3, 'errors': [], 'state': {'players': ['Co', 'stupid'], 'current': 0, 'board': [[28, 35], [27, 36]]}}
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

def test_add():
    assert IA_Game.add((1,1),(2,2))==(3 ,3)
def test_coord():
    assert IA_Game.coord(10) == (1 , 2) 
def test_index():
    assert IA_Game.index((1,2)) == 10
def test_isInside():
    assert IA_Game.isInside((1,2)) == 1 and 2
def test_isGameOver():
    assert IA_Game.isGameOver(request['state']) == False
def test_willBeTaken():
    assert IA_Game.willBeTaken(request['state'],26) == [27]
def test_possibleMove():
    assert IA_Game.possibleMoves(request['state']) == [19,26,37,44]
def test_ApplyMove():
    assert IA_Game.ApplyMove(request['state'],26) == {'players': ['Co', 'stupid'], 'current': 1, 'board': [[28, 35, 26, 27], [36]]}

def test_IAColor():
    assert IA_Game.IAColor(request['state']) == 'black'
def test_OpponentColor():
    assert IA_Game.OpponentColor(request['state']) == 'white'
def test_IATiles():
    assert IA_Game.IATiles(request['state']) == ([28, 35], [27, 36])
def test_MoveValue():
    assert IA_Game.MoveValue(request['state']) == [3,3,3,3]
def test_GetMax():
    assert IA_Game.GetMax(request['state']) == 3
def test_FindMax():
    assert IA_Game.FindMax(request['state']) == [19,26,37,44]
def test_Winner():
    assert IA_Game.Winner(request['state']) == None
def test_Heuristic():
    assert IA_Game.Heuristic(request['state']) == 0
def test_next():
    assert IA_Game.next(request['state']) == 19
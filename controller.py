# implement user input in CFE and some utility
from card import HandCards, Cards
from getkey import getkey, keys
from random import randint, choice
from rule import match


def select(crds): # -> idxSet, zid
    assert type(crds) is HandCards, "TypeError: not HandCards"
    assert 0 < len(crds) <= 5, "IndexError: overrange"
    keyMap = {'Z':0, 'X':1, 'C':2, 'V':3, 'B':4}
    keyStr = "ZXCVB"
    keyStr = keyStr[0:len(crds)] # fix length to n
    print('use [%s] to select:' % keyStr)
    idxSet = set()
    selC, actLst = [], []
    while True:
        k = getkey(blocking=True) # block version
        kn = keys.name(k)
        if len(kn)==1 and kn in keyMap:
            if kn in idxSet: # already in set
                idxSet ^= {keyMap[kn]} # xor, flip
            else:
                idxSet |= {keyMap[kn]} # or, update
            selC = Cards([crds[i] for i in idxSet])
            actLst = match(selC)
            print(selC, actLst)
        elif kn in {'ENTER','SPACE'} and len(actLst)>0:
            if len(actLst) > 1:
                return idxSet, actLst[choose(actLst)]
            else:
                return idxSet, actLst[0]
        elif kn == "ESC":
            idxSet = set()
        else:
            pass

def choose(Lst): # -> i
    assert type(Lst) in {list, HandCards}, "TypeError: not list or HandCards"
    assert 0 < len(Lst) <= 5, "IndexError: overrange"
    keyMap = {'Z':0, 'X':1, 'C':2, 'V':3, 'B':4}
    keyStr = "ZXCVB"
    keyStr = keyStr[0:len(Lst)] # fix length to n
    print('use [%s] to choose:' % keyStr)
    i = -1
    while True:
        k = getkey(blocking=True) # block version
        kn = keys.name(k)
        if len(kn)==1 and kn in keyMap:
            i = keyMap[kn]
            print('>%d' % i)
        elif kn in {'ENTER','SPACE'} and 0 <= i < 5:
            return i
        else:
            pass

def selectR(crds): # -> idxSet, zid
    assert type(crds) is HandCards, "TypeError: not HandCards"
    assert 0 < len(crds) <= 5, "IndexError: overrange"
    bag = list(range(1, 2**len(crds)))
    while True:
        if len(bag) > 0:
            r = randint(0, len(bag)-1) # as index
        else:
            raise RuntimeError("no choice in bag")
        
        selPat = [bag[r] & (2**i) > 0 for i in range(5)] # binary exp
        idxSet = []
        selC = []
        for i in range(5):
            if selPat[i]:
                selC.append(crds[i])
                idxSet.append(i)
        actLst = match(Cards(selC))
        if len(actLst) >= 1:
            return set(idxSet), choice(actLst)
        else:
            del bag[r] # remove this val

def chooseR(Lst): # -> i
    assert type(Lst) in {list, HandCards}, "TypeError: not list or HandCards"
    assert 0 < len(Lst) <= 5, "IndexError: overrange"
    return Lst[randint(0, len(Lst))]

if __name__ == "__main__":
    print("test select()")
    print("idxSet, zid -> ", select(HandCards([1,1,1,2,3])))
    print("test choose()")
    print("i -> ", choose([1,2,3]))
    print("test selectR()")
    print("idxSet, zid -> ", selectR(HandCards([1,1,1,2,3])))
    print("test chooseR()")
    print("i -> ", chooseR([1,2,3]))
    input('enter to exit.') # block prog

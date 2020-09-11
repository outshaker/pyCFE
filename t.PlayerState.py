from card import Deck,HandCards
# from controller import select, choose, selectR, chooseR



class PlayerState:
    def __init__(self, hp=100, shell=None, deck=Deck(), hands=HandCards()):
        self._hp = hp
        self._shell = shell
        self._deck = deck
        self._hands = hands
        self._discarded_card = None
        self._hasCover = False
        self._cover = ""
        self._isDizzy = False
        self._dizzyToken = None

    def hurt(self, val):
        if type(val) is int and val > 0:
            self._hp -= val
        
    def heal(self, val):
        if type(val) is int and val > 0:
            self._hp += val
        
    def shield(self, val):
        if type(val) is int and val > 0:
            self._shell = val
        
    def disperse(self, val):
        if self._shell and type(val) is int and val > 0:
            self._shell = None if val > self._shell else self._shell-val

    def seal(self):
        self._hasCover = True
        self._cover = "seal"
    
    def defense(self):
        self._hasCover = True
        self._cover = "defense"
        
    def refelect(self):
        self._hasCover = True
        self._cover = "refelect"
        
    def empty_fort(self):
        self._hasCover = True
        self._cover = "empty_fort"
        
    def dizzy(self):
        self._isDizzy = True
        self._dizzyToken = 2



    def draw(self, n=2):
        if len(self._hand) + n > 5:  # note: ensure 1 <= n <= 5 - len(self.hand)
            n = 5 - len(self._hand)
        drawC = self._deck.drawn(n)
        self._hand.join(drawC)

    def pickup(self,idxSet):
        return self._hands.pickup(idxSet)
        
    def join(self, crds):
        self._hands.join(crds)

    def discard(card):
        self._discarded_card = card

    def add_to_deck(self, crds):
        self._deck.join(crds)

    def get_hands(self):
        return self._hands

    # def dumps(self): # dump object to json string
    # def loads(s): # load json string to object
    
class PlayerAgent:
    def __init__(self, playStat):
        self._playStat = playStat

    @property
    def hp(self):
        return self._playStat._hp

    @property
    def shell(self):
        return self._playStat._shell
    
    @property
    def hasCover(self):
        return self._playStat._hasCover
    
    @property
    def cover(self):
        return self._playStat._cover

    @property
    def discard_card(self):
        return self._playStat._discarded_card
        
    @property
    def isDizzy(self):
        return self._playStat._isDizzy
    @property
    def dizzyToken(self):
        return self._playStat._dizzyToken

    def exec(self, efctID, val=None):
        e2s = ["無定義", "受傷", "補血", "叫盾", "扣盾", "封印", "防禦", "反震", "空城", "中光芒"]
        e2f = [
            None,
            self._playStat.hurt,
            self._playStat.heal,
            self._playStat.shield,
            self._playStat.disperse,
            self._playStat.seal,
            self._playStat.defense,
            self._playStat.refelect,
            self._playStat.empty_fort,
            self._playStat.dizzy
        ]
        f = e2f[efctID]
        if f and val:
            f(val)
            print(f'INFO: {e2s[efctID]} {val}點')
        elif f:
            f()
            print(f'INFO: {e2s[efctID]}')
        else:
            print('ERROR: undefined efctID')

    def show(self):
        print(f'HP:{self.hp} Shell:{self.shell}')
        if self.hasCover:
            print(f'cover: {self.cover}')
        if self.discard_card:
            print(f'disc: {self.discard_card}')
        if self.isDizzy:
            print(f'dizzy({self.dizzyToken})')

def testAllEfct():
    pstat = PlayerState(10)
    p = PlayerAgent(pstat)
    testCmds = [
        (1,3),
        (2,4),
        (3,10),
        (4,1),
        (5,None),
        (6,None),
        (7,None),
        (8,None),
        (9,None)
    ]
    p.show()
    print("start test")
    for cmd in testCmds:
        p.exec(*cmd)
        p.show()
    print("end test")

# action
# def deal(self):
    # idxSet, zid = selectR(self.hand)
    # selC = self.hand.pickup(idxSet) # Note: pick to match, pickup to deal

# def drawD(self, n=2):
    # if len(self.hand) + n > 6:  # note: ensure 1 <= n <= 6 - len(self.hand)
        # n = 6 - len(self.hand)
    # drawC = HandCards(self.deck.drawn(n + 1))
    # idxSet = {chooseR(drawC)}
    # self.discard = drawC.pickup(idxSet, toCard=True)
    # self.hand.join(drawC)

testAllEfct()


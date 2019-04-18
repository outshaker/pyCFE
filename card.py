#CFE basicXing, card define
from random import randint

class Xing:
    def __init__(self,x):
        xingList="JMSHT"
        assert x in xingList, "Error: %s is not xingTok" % x
        self.xing = x

    def __str__(self):
        xing2str = {'J':"Jin", 'M':"Mu", 'S':"Shui", 'H':"Huo", 'T':"Tu"}
        if self.xing in xing2str: return "Xing('%s')" % xing2str[self.xing]
        else: return ""

    def getId(self):
        xing2i = {'J':0, 'S':1, 'M':2, 'H':3, 'T':4}
        if self.xing in xing2i: return xing2i[self.xing]
        else: return None
    # TODO: compare, shen, ker, reverseShen, reverseKer, same

class Card: # str-based, can be made by crdId
    def __init__(self,x):
        assert type(x) in [str,int,Card],\
        "TypeError: not support type %s" % type(x).__name__
        if type(x) is str and len(x) == 2: # crdStr: G1, S2
            self.crdStr = x
        elif type(x) is int and 1<=x<=25: # use crdId to make Card
            crdId2crdStr = [None, 'J1', 'S1', 'M1', 'H1', 'T1', 'J2', 'S2',
            'M2', 'H2', 'T2', 'J3', 'S3', 'M3', 'H3', 'T3', 'J4', 'S4', 'M4',
            'H4', 'T4', 'J5', 'S5', 'M5', 'H5', 'T5']
            self.crdStr = crdId2crdStr[x]
        elif type(x) is Card: # [!] note: use Card to make Card
            self.crdStr = x.crdStr
        else:
            raise TypeError("Bad argument for Card()") # die faster

    def __str__(self): return "'%s'" % self.crdStr
    def __repr__(self): return "Card('%s')" % self.crdStr

    def getXingTok(self): return self.crdStr[0]
    def getXingId(self):
        xing2i = {'J':0, 'S':1, 'M':2, 'H':3, 'T':4}
        return xing2i[self.crdStr[0]]
    def getXing(self): return Xing(self.crdStr[0])
    def getLv(self): return int(self.crdStr[1])
    def getId(self): # cover str to int
        xing2i = {'J':0, 'S':1, 'M':2, 'H':3, 'T':4}
        if self.crdStr[0] in xing2i: xing = xing2i[self.crdStr[0]]
        else: return None
        lv = int(self.crdStr[1])
        return xing* 4 + lv

def _isCardList(lst): # check list of Card
    if type(lst) is list:
        t = [type(e) is Card for e in lst]
        return all(t)
    else:
        return False
class Cards: # for Deck, Hand, data: [card(), ...]
    def __init__(self,x=None): # allow Cards, CardList, cidList, tokList and None
        if x is None:
            self.lst = []
        elif type(x) is Cards:
            self.lst = x.lst.copy()
        elif _isCardList(x):
            self.lst = x.copy() # CardList[].copy()
        elif type(x) is list and type(x[0]) in [int, str]:
            self.lst = list(map(Card,x))
        else:
            raise TypeError("Bad argument for Cards()") # die faster
    def __str__(self):
        s='Cards(['
        for i in range(len(self.lst)):
            if i==0:
                s = s+str(self[i])
            else:
                s = s+', '+str(self[i])
        s = s+'])'
        return s
    def __repr__(self):
        s='Cards(['
        for i in range(len(self.lst)):
            if i==0:
                s = s + repr(self[i])
            else:
                s = s+', '+ repr(self[i])
        s = s+'])'
        return s
    
    def __len__(self): return len(self.lst)
    def __getitem__(self,k): return Card(self.lst[k])
    # def __setitem__(self,k,v): self.lst[k]=v
    # def __delitem__(self,k): del self.lst[k]
    
    # def pop(self,i=None):
    #     if i is None: i = len(self) - 1
    #     return self.lst.pop(i)
    # def append(self,e):
    #     assert type(e) is Card, "TypeError: %s is not Card" % e
    #     self.lst.append(e)
    
    def drawn(self,n=1): # -> drawC#CardList
        assert len(self)>0, "RuntimeError: empty list"
        if n > len(self):
            print("drawn(%d): fix n to %d" % (n,len(self)))
            n = len(self) # fix n to len(crds)
        # TODO: implment slicable list, __getitem__() slice object
        drawC, self.lst = self.lst[-n:], self.lst[:-n] # direct use inner data, I tired...
        return Cards(drawC)

    def join(self,crds): # exec, add crds to self
        if isinstance(crds,Cards): # as crds
            self.lst.extend(crds.lst)
        elif _isCardList(crds): # as crdLst
            self.lst.extend(crds)
        elif type(crds) is Card: # as crd
            self.lst.append(crds)
        else:
            raise TypeError("Bad argument")

class HandCards(Cards):
    def __init__(self, crds=None):
        super().__init__(crds)
        # print(type(self))
        # print(self.lst)
    def _inverse(self, idxSet): # -> idxSet(inversed)
        return set(range(len(self))) - idxSet
    def pick(self, idxSet): # -> pickCrds#HandCards
        # assert all([0 <= x < len(self) for x in idxSet]), "ValueError: invalid index"
        idxSet = list(filter(lambda x:0 <= x < len(self), idxSet)) # get safe index
        pickCrds = [self[i] for i in idxSet]
        return Cards(pickCrds)
    def pickup(self, idxSet): # -> pickCrds#HandCards, move out pickCrds like stack POP
        invrsSet = self._inverse(idxSet)
        pickCrds, restCrds = self.pick(idxSet), self.pick(invrsSet)
        self.lst = restCrds.lst
        return pickCrds

    # def divide(self, idxSet): # -> pickLst, restLst
    #     invrsSet = self._inverse(idxSet)
    #     return self.pick(idxSet), self.pick(invrsSet)
class Deck(Cards):
    def _makeDeckIdList(self, idPat): # for deck
        idLst = []
        for i in range(len(idPat)):
            idLst.extend([i]*idPat[i])
        print('_makeDeckIdList(): idLst-> ',idLst)
        # suffle
        def _swap(lst,x,y):
            lst[x], lst[y] = lst[y], lst[x]
        n = len(idLst)
        for i in range(n):
            _swap(idLst, i, randint(0,n-1))
        print('_makeDeckIdList(): suffled idLst-> ',idLst)
        return idLst

    def __init__(self, idPat=None):
        if idPat:
            self.idPat = idPat
        else:
            self.idPat = [0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3]
        idLst = self._makeDeckIdList(self.idPat)
        super().__init__(idLst)
        
    def drawn(self,n):
        if len(self.lst)<n:
            print('deck.drawn(): make new deck')
            newDeck = Deck(self.idPat)
            newDeck.join(self)
            self.lst = newDeck.lst
            print('deck.drawn(): deck-> ',self)
        return super().drawn(n)

if __name__ == '__main__':        
    # test module
    def testXing(x):
        assert type(x) is Xing, "TypeError: not Xing"
        print(x)
        print(x.getId())
        
    def testCard(c):
        assert type(c) is Card, "TypeError: not Card"
        print(c)
        print('repr -> ',repr(c))
        print(c.getXingTok())
        print(c.getXing())
        print(c.getLv())
        print(c.getId())
        
    def testCards(crds):
        assert type(crds) is Cards, "TypeError: not Cards"
        print(crds)
        print('repr -> ', repr(crds))
        print('len() -> ', len(crds))
        print('crds.lst= ', crds.lst)
        print('test crds[i]')
        for i in range(len(crds)):
            print(crds[i])
        print('test join()')
        crds.join(Card("H3"))
        print('after join(Card("H3"), crds -> ', crds)
        print('test drawn()')
        print('drawn() -> ', crds.drawn())
        print('after drawn(), crds ->', crds)
        print('test drawn up & join back')
        d = crds.drawn(3)
        print('after drawn(3), crds adn d -> ', crds, d)
        crds.join(d)
        print('join back, crds -> ', crds)

    def testCardList(crdLst):
        print("test Cards(crdLst)")
        print("crdLst= ",crdLst)
        print("_isCardList(crdLst) -> ",_isCardList(crdLst))

    def testHandCards(hcrds):
        assert type(hcrds) is HandCards, "TypeError: not HandCards"
        print(hcrds)
        print('repr -> ',repr(hcrds))
        print('pick({1,2}) -> ',hcrds.pick({1,2}))
        print('pickup({1,2}) -> ',hcrds.pickup({1,2}))
        print('after pickup({1,2}), hcrds -> ',hcrds)
    def testDeckHand(deck,hand): # as (Cards, Cards)
        print('test deck & hand')
        print('deck,hand= ', deck, hand)
        d=deck.drawn(1)
        print('deck.drawn(1)->d')
        print('deck,hand,d= ', deck, hand, d)
        print('hand.join(d)')
        hand.join(d)
        print('deck,hand,d= ', deck, hand, d)
    def testDeck(): # Deck(Cards)
        idPat = [0,1,1,2] # test: 4 card, 3 element
        deck = Deck(idPat)
        print('deck= ', deck)
        print('deck.drawn(3)-> ', deck.drawn(3))
        print('deck.drawn(3)-> ', deck.drawn(3))

    testXing(Xing('J'))
    testCard(Card('J5'))
    testCard(Card(randint(1,25)))
    testCards(Cards([10,15,12,13,8]))
    crdLst = [Card(i) for i in [10,15,12,13,8]]
    testCardList(crdLst)
    deck, hand = Cards([1,2,3,4,5]), Cards()
    testDeckHand(deck,hand)
    testDeck()

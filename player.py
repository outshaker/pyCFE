# CFE player
from card import Cards, HandCards, Deck
from controller import select, choose, selectR, chooseR


class Player:
    def __init__(self, name, deck, discPile, tokList=None):
        assert type(deck) is Deck, "TypeError: not Deck"
        self.name = name
        self.deck = deck
        self.discPile = discPile
        if tokList:
            self.hand = HandCards(tokList)
        else:
            self.hand = HandCards(deck.drawn(5))

    def __str__(self):
        return 'Player("%s", %s)' % (self.name, str(self.hand))

    def __repr__(self):
        return 'Player("%s", %s)' % (self.name, repr(self.hand))

    def _clearHand(self):  # exec, DEV utility
        print("_clearHand(): clear hand")
        self.hand = HandCards()

    def deal(self):  # exec, select, match, deal
        # print("deal(): hand-> ", self.hand)
        idxSet, zid = selectR(self.hand)
        selC = self.hand.pickup(idxSet) # Note: pick to match, pickup to deal
        print("deal(): selC, zid -> ", selC, zid)
        # ruleSys.effect(self, selC, zid) # TODO: send play[selC,zid] to rule

    def draw(self, n=2):  # exec, deck--drawC->hand
        if len(self.hand) + n > 5:  # note: ensure 1 <= n <= 5 - len(self.hand)
            print("p.draw(%d): fix n to %d" % (n, 5 - len(self.hand)))
            n = 5 - len(self.hand)
        drawC = self.deck.drawn(n)
        print("draw(): drawC -> ", drawC)
        self.hand.join(drawC)

    def drawD(self, n=2):
        # draw with discard, deck--drawC-> hand, discPile
        if len(self.hand) + n > 6:  # note: ensure 1 <= n <= 6 - len(self.hand)
            print("p.draw(%d): fix n to %d" % (n, 6 - len(self.hand)))
            n = 6 - len(self.hand)
        drawC = HandCards(self.deck.drawn(n + 1))
        # Note: need pickup(), change to HandCards
        idxSet = {chooseR(drawC)}
        disc = drawC.pickup(idxSet)
        print("drawWD(): drawC, disc ->", drawC, disc)
        self.discPile.join(disc)  # drop one card
        self.hand.join(drawC)  # drawC >> hand

    def action(self):  # exec, deal and draw
        print("player(%s) action" % self.name)
        self.deal()
        self.draw()
        # self.drawD(deck)
        # note: let upper object contorl turn


if __name__ == "__main__":

    deck = Cards([13, 12, 11, 10, 9, 8, 7, 6])
    deck = Deck([0, 1, 1, 1, 1, 1, 1, 1, 1])
    disP = Cards()
    p = Player("s", deck, disP, [1, 2, 3])
    print(p)
    p.deal()
    print("after deal()", p)

    print("draw(1) from deck")
    p.draw(1)
    print("p,deck= ", p, deck)
    p._clearHand()

    print("draw(2) from deck")
    p.draw(2)
    print("p,deck= ", p, deck)
    p._clearHand()

    print("drawD(3) from deck")
    p.drawD(3)
    print("p,deck= ", p, deck)
    p._clearHand()

    print("drawD(2) from deck")
    p.drawD()
    print("p,deck= ", p, deck)

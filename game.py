# game object, use ring to keep game running
from card import Deck, Cards
from player import Player
from ring import Ring
from time import sleep

deck = Deck()
disP = Cards()
p1 = Player("A", deck, disP)
p2 = Player("B", deck, disP)
players = Ring([p1, p2])
turn = 0

while True:
    turn = turn + 1
    print("turn#%d " % turn, end='')
    players.now().action()
    players.goNext()
    sleep(1)

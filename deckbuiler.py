# DeckBuilder class for building and managing the deck of cards for solitaire game
import random
from time import time
from card import Card

class DeckBuilder:
    def __init__(self, seed: int = None):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)

    def print_deck(self):
        for card in self.cards:
            print(card)




if __name__ == "__main__":
    # Create a seed based on the computer time in ticks
    seed = int(time() * 1000)
    deck = DeckBuilder(seed)
    deck.print_deck()

    seed = 42 
    deck2 = DeckBuilder(seed)
    deck2.print_deck()

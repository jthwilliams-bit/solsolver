from enum import Enum

class Position(Enum):
    Foundation1 = "f1"
    Foundation2 = "f2"
    Foundation3 = "f3"
    Foundation4 = "f4"
    Waste = "waste"
    Stock = "stock"
    Column1 = "c1"
    Column2 = "c2"
    Column3 = "c3"
    Column4 = "c4"
    Column5 = "c5"
    Column6 = "c6"
    Column7 = "c7"

class KlondikeMove:
    def __init__(self, source: Position, destination: Position, num_cards: int = 1):
        self.source = source
        self.destination = destination
        self.num_cards = num_cards

    def __repr__(self):
        return f"Move {self.num_cards} card(s) from {self.source.value} to {self.destination.value}"
    
if __name__ == "__main__":

    pos = Position["Foundation1"]
    print(pos)

    

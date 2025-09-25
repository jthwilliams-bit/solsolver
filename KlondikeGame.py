from typing import Optional
from solitairgame import SolitaireGame
from card import Card
from deckbuiler import DeckBuilder
from KlondikeMove import Position, KlondikeMove


class KlondikeGame(SolitaireGame):



    def __init__(self, seed: Optional[int] = None, draw_count: Optional[int] = 1):
        super().__init__()
        self.initialize_klondike_board(seed=seed, draw_count=draw_count)



    def initialize_klondike_board(self, seed: Optional[int] = None, draw_count: Optional[int] = 1):
        self.deck = DeckBuilder(seed=seed)
        self.stock = []
        self.waste = []
        self.tableau = [[] for _ in range(7)]
        self.tableau_face_up = [[] for _ in range(7)]  # number of face-up cards in each tableau pile
        self.foundation = [[] for _ in range(4)]  # one for each suit
        self.draw_count = draw_count  # number of cards to draw from stock to waste
        

        
        # Initialize a Klondike specific board setup
        self.board = [[' ' for _ in range(7)] for _ in range(7)]
        # Add specific Klondike setup logic here

    def deal(self):
        # Implement Klondike specific dealing logic
        print("Dealing cards in Klondike style.")
        # Add dealing logic here
        for i in range(7):
            for j in range(i, 7):
                card = self.deck.cards.pop() if self.deck.cards else None
                if card:
                    self.tableau[j].append(card)
        for i in range(7):
            if self.tableau[i]:
                self.tableau_face_up[i].append(self.tableau[i].pop())


    def draw_layout_console(self):

        # for the stock pile show the number of cards left
        print(f"Stock: {len(self.deck.cards)} cards left")
        #for the waste pile show the top card 3 cards if any
        if self.waste:
            for i in range(min(3, len(self.waste))):
                if i == 0:
                    print(f"Waste top: {self.waste[-1 - i]}")
                else:
                    print(f"Waste {i+1}: {self.waste[-1 - i]}")
        else:
            print("Waste: Empty")


        # for the home piles show the top card if any or show empty

        row_home_str = "Home Row: "
        for i in range(4):

            if self.foundation[i]:
                str_card = str(self.foundation[i][-1])
                if len(str_card) > 10:
                    str_card = "[" + str_card[:9] + ".]"
                row_home_str += str_card.ljust(10) if len(str_card) < 10 else str_card
            else:
                row_home_str += "[   Empty   ]"
        print(row_home_str)


        # for i to n show the card if any in the tableau piles until there are no cards in any of the piles
        for i in range(0, max(len(pile) + len(face_up) for pile, face_up in zip(self.tableau, self.tableau_face_up))):
            row = []
            for j in range(7):
                if i < len(self.tableau[j]):
                    card_str = str(self.tableau[j][i])
                    card_str = "~" +card_str[:9] + ".~"
                    if len(card_str) > 12:
                        card_str = "~" +card_str[:9] + ".~"

                    row.append(card_str.ljust(12) if len(card_str) < 12 else card_str)
                else:
                    if i < len(self.tableau_face_up[j]) + len(self.tableau[j]):
                        card_str = str(self.tableau_face_up[j][i - len(self.tableau[j])])
                        if len(card_str) > 12:
                            card_str =  card_str[:9] + "."
                        row.append(card_str.ljust(12) if len(card_str) < 12 else card_str)
                    else:
                        row.append("            ")
            print(" | ".join(row))

    
    def move (self, move: KlondikeMove) -> bool:
        # Case 1: moving from tableau to tableau
        if move.source in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                                Position.Column5, Position.Column6, Position.Column7] and \
           move.destination in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                                Position.Column5, Position.Column6, Position.Column7]:
            return self.move_tableau_to_tableau(move)      
        return False

    
    def move_tableau_to_tableau(self, move: KlondikeMove) -> bool:
        source_index = -1
        dest_index = -1
        
        # check if the move is from a tableau 
        if move.source in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                           Position.Column5, Position.Column6, Position.Column7]:
            source_index = move.source.value[-1]  # get the column number from the position
            print(f"Source index: {source_index}")
        
        if move.destination in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                                Position.Column5, Position.Column6, Position.Column7]:
            dest_index = move.destination.value[-1]  # get the column number from the position
            print(f"Destination index: {dest_index}")
        # check that there are enough face-up cards in the source tableau
        if source_index != -1 and dest_index != -1:
            if move.num_cards > len(self.tableau_face_up[int(source_index)-1]):
                print(f"Not enough face-up cards in source tableau {source_index}")
                return False
            # check that the move follows Klondike rules (alternating colors, descending rank)
            moving_cards = self.tableau_face_up[int(source_index)-1][-move.num_cards:]
            if not moving_cards:
                print("No cards to move")
                return False
            if dest_index != -1:
                if self.tableau_face_up[int(dest_index)-1]:
                    dest_card = self.tableau_face_up[int(dest_index)-1][-1]
                    if (Card.RANKS.index(moving_cards[0].rank) != Card.RANKS.index(dest_card.rank) - 1 or
                        moving_cards[0].color == dest_card.color):
                        print("Move does not follow Klondike rules")
                        return False
                else:
                    if moving_cards[0].rank != 'K':
                        print("Only a King can be moved to an empty tableau")
                        return False
            # For each card being moved, pop it from the source and append to the destination
            for _ in range(move.num_cards):
                card = self.tableau_face_up[int(source_index)-1].pop()
                self.tableau_face_up[int(dest_index)-1].append(card)
            #if there are no more face-up cards in the source tableau, flip the top card of the source tableau if any
            if not self.tableau_face_up[int(source_index)-1] and self.tableau[int(source_index)-1]:
                card = self.tableau[int(source_index)-1].pop()
                self.tableau_face_up[int(source_index)-1].append(card)
        return True


if __name__ == "__main__":
    game = KlondikeGame(seed=42)
    game.deal()
    game.draw_layout_console()


    game.move(KlondikeMove(Position.Column1, Position.Column3, 1))
    game.move(KlondikeMove(Position.Column4, Position.Column5, 1))

    game.draw_layout_console()



    # # while 'e' not entered get a move from the user and validate it
    # while True:
    #     user_input = input("Enter move (e to exit) in format 'source destination num_cards': ")
    #     if user_input.lower() == 'e':
    #         break
    #     try:
    #         source_str, dest_str, num_cards_str = user_input.split()
    #         source = Position[source_str]
    #         destination = Position[dest_str]
    #         num_cards = int(num_cards_str)
    #         move = KlondikeMove(source, destination, num_cards)
    #         if game.validate_move(move):
    #             print("Move is valid.")
    #         else:
    #             print("Move is invalid.")
    #     except Exception as e:
    #         print(f"Error processing move: {e}")
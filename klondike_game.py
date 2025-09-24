from solitairgame import SolitaireGame
from card import Card
from deckbuiler import DeckBuilder


class KlondikeGame(SolitaireGame):



    def __init__(self):
        super().__init__()
        
        
        self.initialize_klondike_board()



    def initialize_klondike_board(self):
        self.deck = DeckBuilder()
        self.stock = []
        self.waste = []
        self.tableau = [[] for _ in range(7)]
        self.tableau_face_up = [[] for _ in range(7)]  # number of face-up cards in each tableau pile
        self.home = [[] for _ in range(4)]  # one for each suit

        
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

            if self.home[i]:
                str_card = str(self.home[i][-1])
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





    def move(self, from_pos, to_pos):
        # Implement Klondike specific move logic
        print(f"Moving from {from_pos} to {to_pos} in Klondike style.")
        # Add move validation and execution logic here

    def is_game_over(self):
        # Implement Klondike specific game over logic
        return False
    
if __name__ == "__main__":
    game = KlondikeGame()
    game.deal()
    game.draw_layout_console()
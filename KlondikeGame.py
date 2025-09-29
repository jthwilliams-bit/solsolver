from typing import Optional
from solitairgame import SolitaireGame
from card import Card
from deckbuiler import DeckBuilder
from KlondikeMove import Position, KlondikeMove
import json
import os


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
                    print(f"Waste top: {self.waste[-1 - i].FormatedforConsole()}")
                else:
                    print(f"Waste {i+1}: {self.waste[-1 - i].FormatedforConsole()}")
        else:
            print("Waste: Empty")


        # for the home piles show the top card if any or show empty

        row_home_str = "Home Row: "
        for i in range(4):

            if self.foundation[i]:
                str_card = str(self.foundation[i][-1].FormatedforConsole())
                if len(str_card) > 10:
                    str_card = "[" + str_card + " ]"
                row_home_str += str_card.ljust(10) if len(str_card) < 10 else str_card
            else:
                row_home_str += "[~  ~]"
        print(row_home_str)


        # for i to n show the card if any in the tableau piles until there are no cards in any of the piles
        for i in range(0, max(len(pile) + len(face_up) for pile, face_up in zip(self.tableau, self.tableau_face_up))):
            row = []
            for j in range(7):
                if i < len(self.tableau[j]):
                    card_str = str(self.tableau[j][i].FormatedforConsole())
                    card_str = "~" +card_str + "~"


                    row.append(card_str.ljust(12) if len(card_str) < 12 else card_str)
                else:
                    if i < len(self.tableau_face_up[j]) + len(self.tableau[j]):
                        card_str = str(self.tableau_face_up[j][i - len(self.tableau[j])].FormatedforConsole())
                        card_str = " " +card_str + " "

                        row.append(card_str)
                    else:
                        row.append("     ")
            print(" | ".join(row))

    
    def move (self, move: KlondikeMove) -> bool:
        # Case 1: moving from tableau to tableau
        if move.source in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                                Position.Column5, Position.Column6, Position.Column7] and \
           move.destination in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                                Position.Column5, Position.Column6, Position.Column7]:
            return self.move_tableau_to_tableau(move)      
        
        # Case 2: moving from stock to waste
        elif move.source == Position.Stock and move.destination == Position.Waste:
            return self.move_stock_to_waste(move)
        # Case 3: moving from waste to tableau 
        elif move.source == Position.Waste and move.destination in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                                Position.Column5, Position.Column6, Position.Column7]:
            return self.move_waste_to_column(move)
        # Case 4: moving from tableau to foundation
        elif move.source in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                                Position.Column5, Position.Column6, Position.Column7] and \
                move.destination in [Position.Foundation1, Position.Foundation2, Position.Foundation3, Position.Foundation4]:
            return self.move_column_to_foundation(move)
        # Case 5: moving from foundation to tableau
        elif move.source in [Position.Foundation1, Position.Foundation2, Position.Foundation3, Position.Foundation4] and \
                move.destination in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                                Position.Column5, Position.Column6, Position.Column7]:
            print("Moving from foundation to tableau")
            return self.move_foundation_to_column(move)
        # Case 6: moving from waste to foundation
        elif move.source == Position.Waste and move.destination in [Position.Foundation1, Position.Foundation2, Position.Foundation3, Position.Foundation4]:
            return self.move_waste_to_foundation(move)
        
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
            tmp = []
            for _ in range(move.num_cards):
                card = self.tableau_face_up[int(source_index)-1].pop()
                print(f"Moving card: {card}")
                tmp.append(card)

            for _ in range(move.num_cards):
                card = tmp.pop()
                print(f"Moving card: {card}")
                self.tableau_face_up[int(dest_index)-1].append(card)
            #if there are no more face-up cards in the source tableau, flip the top card of the source tableau if any
            if not self.tableau_face_up[int(source_index)-1] and self.tableau[int(source_index)-1]:
                card = self.tableau[int(source_index)-1].pop()
                self.tableau_face_up[int(source_index)-1].append(card)
        return True

    def move_tableau_to_foundation(self, move: KlondikeMove) -> bool:
        source_index = -1
        dest_index = -1
        
        # check if the move is from a tableau 
        if move.source in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                           Position.Column5, Position.Column6, Position.Column7]:
            source_index = move.source.value[-1]  # get the column number from the position
            print(f"Source index: {source_index}")
        
        if move.destination in [Position.Foundation1, Position.Foundation2, Position.Foundation3, Position.Foundation4]:
            dest_index = move.destination.value[-1]  # get the foundation number from the position
            print(f"Destination index: {dest_index}")
        # check that there are enough face-up cards in the source tableau
        if source_index != -1 and dest_index != -1:
            if move.num_cards != 1 or len(self.tableau_face_up[int(source_index)-1]) < 1:
                print(f"Can only move one card to foundation from tableau {source_index}")
                return False
            moving_card = self.tableau_face_up[int(source_index)-1][-1]
            if not moving_card:
                print("No card to move")
                return False
            # check that the move follows Klondike rules (same suit, ascending rank)
            if self.foundation[int(dest_index)-1]:
                dest_card = self.foundation[int(dest_index)-1][-1]
                if (Card.RANKS.index(moving_card.rank) != Card.RANKS.index(dest_card.rank) + 1 or
                    moving_card.suit != dest_card.suit):
                    print("Move does not follow Klondike rules")
                    return False
            else:
                if moving_card.rank != 'A':
                    print("Only an Ace can be moved to an empty foundation")
                    return False
            # Move the card from tableau to foundation
            card = self.tableau_face_up[int(source_index)-1].pop()
            self.foundation[int(dest_index)-1].append(card)
            #if there are no more face-up cards in the source tableau, flip the top card of the source tableau if any
            if not self.tableau_face_up[int(source_index)-1] and self.tableau[int(source_index)-1]:
                card = self.tableau[int(source_index)-1].pop()
                return True
        return False

    def move_stock_to_waste(self, move: KlondikeMove) -> bool:
        if move.source == Position.Stock and move.destination == Position.Waste:
            if not self.deck.cards:
                # if the stock is empty restock the stock from the waste pile
                # if waste is also empty do nothing and return false
                if not self.waste:
                    print("Both stock and waste are empty, cannot move")
                    return False
                self.deck.cards = self.waste[::-1]  # reverse the waste to maintain order
                self.waste = []
                print("Restocked the stock from the waste pile")
                return False
            for _ in range(self.draw_count if self.draw_count and self.draw_count > 0 else 1):
                if self.deck.cards:
                    card = self.deck.cards.pop()
                    self.waste.append(card)
                    print(f"Moved card {card} from stock to waste")
            return True
        return False

    def move_waste_to_column(self, move: KlondikeMove) -> bool:
        if move.source in [ Position.Waste] and move.destination in [Position.Column1, Position.Column2, 
                                                                     Position.Column3, Position.Column4, Position.Column5,
                                                                      Position.Column6, Position.Column7 ]:
            if self.waste:
                #check the waste card is 1 rank down and opposite color to the card on the bottome of the destination face up pile
                dest_index = move.destination.value[-1]
                waste_card = self.waste[-1]
                if self.tableau_face_up[int(dest_index)-1]:
                    dest_card = self.tableau_face_up[int(dest_index)-1][-1]
                    if (Card.RANKS.index(waste_card.rank) != Card.RANKS.index(dest_card.rank) - 1 or
                        waste_card.color == dest_card.color):
                        print("Move does not follow Klondike rules")
                        return False
                else:
                    if waste_card.rank != 'K':
                        print("Only a King can be moved to an empty column")
                        return False

                card = self.waste.pop()
                dest_index = move.destination.value[-1]
                self.tableau_face_up[int(dest_index)-1].append(card)
                print(f"Moved card {card} from waste to column {move.destination}")
                return True
        return False
        
    def move_column_to_foundation(self, move: KlondikeMove) -> bool:
        source_index = -1
        dest_index = -1
        
        # check if the move is from a tableau 
        if move.source in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                           Position.Column5, Position.Column6, Position.Column7]:
            source_index = move.source.value[-1]  # get the column number from the position
            print(f"Source index: {source_index}")
        
        if move.destination in [Position.Foundation1, Position.Foundation2, Position.Foundation3, Position.Foundation4]:
            dest_index = move.destination.value[-1]  # get the foundation number from the position
            print(f"Destination index: {dest_index}")
        # check that there are enough face-up cards in the source tableau
        if source_index != -1 and dest_index != -1:
            if move.num_cards != 1 or len(self.tableau_face_up[int(source_index)-1]) < 1:
                print(f"Can only move one card to foundation from tableau {source_index}")
                return False
            moving_card = self.tableau_face_up[int(source_index)-1][-1]
            if not moving_card:
                print("No card to move")
                return False
            # check that the move follows Klondike rules (same suit, ascending rank)
            if self.foundation[int(dest_index)-1]:
                dest_card = self.foundation[int(dest_index)-1][-1]
                if (Card.RANKS.index(moving_card.rank) != Card.RANKS.index(dest_card.rank) + 1 or
                    moving_card.suit != dest_card.suit):
                    print("Move does not follow Klondike rules")
                    return False
            else:
                if moving_card.rank != 'A':
                    print("Only an Ace can be moved to an empty foundation")
                    return False
            # Move the card from tableau to foundation
            card = self.tableau_face_up[int(source_index)-1].pop()
            self.foundation[int(dest_index)-1].append(card)
            #if there are no more face-up cards in the source tableau, flip the top card of the source tableau if any
            if not self.tableau_face_up[int(source_index)-1] and self.tableau[int(source_index)-1]:
                card = self.tableau[int(source_index)-1].pop()
                self.tableau_face_up[int(source_index)-1].append(card)
            return True
        return False


    def move_foundation_to_column(self, move: KlondikeMove) -> bool:
        source_index = -1
        dest_index = -1
        
        # check if the move is from a foundation 
        if move.source in [Position.Foundation1, Position.Foundation2, Position.Foundation3, Position.Foundation4]:
            source_index = move.source.value[-1]  # get the foundation number from the position
            print(f"Source index: {source_index}")
        
        if move.destination in [Position.Column1, Position.Column2, Position.Column3, Position.Column4, 
                                Position.Column5, Position.Column6, Position.Column7]:
            dest_index = move.destination.value[-1]  # get the column number from the position
            print(f"Destination index: {dest_index}")
        # check that there are enough cards in the source foundation
        if source_index != -1 and dest_index != -1:
            if move.num_cards != 1 or len(self.foundation[int(source_index)-1]) < 1:
                print(f"Can only move one card from foundation {source_index}")
                return False
            moving_card = self.foundation[int(source_index)-1][-1]
            if not moving_card:
                print("No card to move")
                return False
            # check that the move follows Klondike rules (alternating colors, descending rank)
            if self.tableau_face_up[int(dest_index)-1]:
                dest_card = self.tableau_face_up[int(dest_index)-1][-1]
                if (Card.RANKS.index(moving_card.rank) != Card.RANKS.index(dest_card.rank) - 1 and
                    moving_card.color == dest_card.color):
                    print(moving_card.rank, dest_card.rank, moving_card.color, dest_card.color)
                    print("Move does not follow Klondike rules____")
                    return False
            else:
                if moving_card.rank != 'K':
                    print("Only a King can be moved to an empty tableau")
                    return False
            # Move the card from foundation to tableau
            card = self.foundation[int(source_index)-1].pop()
            self.tableau_face_up[int(dest_index)-1].append(card)
            print(f"Moved card {card} from foundation {move.source} to column {move.destination}")
            return True
        return False


    def move_waste_to_foundation(self, move: KlondikeMove) -> bool:
        if move.source == Position.Waste and move.destination in [Position.Foundation1, Position.Foundation2, Position.Foundation3, Position.Foundation4]:
            if len(self.waste) < 1 or move.num_cards != 1:
                print("Can only move one card from waste to foundation")
                return False
            moving_card = self.waste[-1]
            dest_index = move.destination.value[-1]
            if self.foundation[int(dest_index)-1]:
                dest_card = self.foundation[int(dest_index)-1][-1]
                if (Card.RANKS.index(moving_card.rank) != Card.RANKS.index(dest_card.rank) + 1 or
                    moving_card.suit != dest_card.suit):
                    print("Move does not follow Klondike rules")
                    return False
            else:
                if moving_card.rank != 'A':
                    print("Only an Ace can be moved to an empty foundation")
                    return False
            card = self.waste.pop()
            self.foundation[int(dest_index)-1].append(card)
            print(f"Moved card {card} from waste to foundation {move.destination}")
            return True
        return False


    def save_game(self, filename: str):
        # Prepare the Layout.json template structure
        layout = {
            "Properties": {
            "Type": "Klondike",
            "Sead": str(getattr(self.deck, "seed", "unknown")),
            "Moves": 0,
            "Waste": self.draw_count
            },
            "Cards": {
            "Home": {"1": [], "2": [], "3": [], "4": []},
            "Columns": {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": []},
            "Stock": [],
            "Waste": []
            },
            "Moves": []
        }

        # Helper to convert Card to Layout.json format
        def card_to_layout(card, face_up=True):
            return {
            "Color": card.color,
            "Suit": card.suit,
            "Value": card.rank if card.rank != '10' else '10',
            "FaceUp": face_up
            }

        # Fill Home (foundations)
        for i in range(4):
            layout["Cards"]["Home"][str(i+1)] = [
            card_to_layout(card, True) for card in self.foundation[i]
            ]

        # Fill Columns (tableau)
        for i in range(7):
            pile = []
            # Face-down cards
            for card in self.tableau[i]:
                pile.append(card_to_layout(card, False))
            # Face-up cards
            for card in self.tableau_face_up[i]:
                pile.append(card_to_layout(card, True))
            layout["Cards"]["Columns"][str(i+1)] = pile

        # Fill Stock
        layout["Cards"]["Stock"] = [
            card_to_layout(card, False) for card in self.deck.cards
        ]

        # Fill Waste
        layout["Cards"]["Waste"] = [
            card_to_layout(card, True) for card in self.waste
        ]

        # Save to file named after the seed
        seed_str = str(getattr(self.deck, "seed", "unknown"))
        out_file = f"{seed_str}.json"
        with open(out_file, "w") as f:
            json.dump(layout, f, indent=2)
        print(f"Game saved to {out_file}")


    def load_game(self, filename: str):
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            return False
        with open(filename, "r") as f:
            layout = json.load(f)
        # Load properties
        properties = layout.get("Properties", {})
        self.draw_count = int(properties.get("Waste", 1))
        seed_str = properties.get("Sead", "unknown")
        try:
            seed = int(seed_str)
        except ValueError:
            seed = None
        self.initialize_klondike_board_from_layout(layout, seed=seed)
        return True       
    def initialize_klondike_board_from_layout(self, layout: dict, seed: Optional[int] = None):  
        cards_section = layout.get("Cards", {})
        # Load Home (foundations)
        home = cards_section.get("Home", {})
        for i in range(4):
            self.foundation[i] = [
                Card(card_info["Suit"], card_info["Value"]) for card_info in home.get(str(i+1), [])
            ]
        # Load Columns (tableau)
        columns = cards_section.get("Columns", {})
        for i in range(7):
            pile = columns.get(str(i+1), [])
            self.tableau[i] = []
            self.tableau_face_up[i] = []
            for card_info in pile:
                card = Card(card_info["Suit"], card_info["Value"])
                if card_info.get("FaceUp", False):
                    self.tableau_face_up[i].append(card)
                else:
                    self.tableau[i].append(card)
        # Load Stock
        stock = cards_section.get("Stock", [])
        self.deck.cards = [Card(card_info["Suit"], card_info["Value"]) for card_info in stock]
        # Load Waste
        waste = cards_section.get("Waste", [])
        self.waste = [Card(card_info["Suit"], card_info["Value"]) for card_info in waste]


if __name__ == "__main__":


    def parse_position(pos_str: str) -> Optional[Position]:
        pos_str = pos_str.upper()
        if pos_str == 'S':
            return Position.Stock
        elif pos_str == 'W':
            return Position.Waste
        else:        
            for mem in Position.__members__.values():
                if mem.value.upper() == pos_str:
                    return mem

        return None


    game = KlondikeGame(seed=42)
    game.deal()
    game.draw_layout_console()

    
    print("\nMaking some moves...\n")
    print( "-------------------" )
    game.move(KlondikeMove(Position.Column1, Position.Column3, 1))
    print( "-------------------" )

    game.move(KlondikeMove(Position.Column4, Position.Column5, 1))
    print( "-------------------" )


    game.move(KlondikeMove(Position.Column3, Position.Column7, 2))
    print( "-------------------" )

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    print( "-------------------" )

    game.draw_layout_console()

    game.move(KlondikeMove(Position.Waste, Position.Column5, 1))
    print( "-------------------" )

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    print( "-------------------" )

    game.move(KlondikeMove(Position.Column2, Position.Column6, 1))
    print( "-------------------" )

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    print( "-------------------" )

    game.move(KlondikeMove(Position.Waste, Position.Column7, 1))

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    print( "-------------------" )

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    print( "-------------------" )
    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))


    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    game.move(KlondikeMove(Position.Waste, Position.Column5, 1))

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    game.move(KlondikeMove(Position.Waste, Position.Column3, 1))

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))

    game.move(KlondikeMove(Position.Waste, Position.Column6, 1))

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    game.move(KlondikeMove(Position.Waste, Position.Column1, 1))
    game.move(KlondikeMove(Position.Column4, Position.Column1, 1))
    game.move(KlondikeMove(Position.Column5, Position.Column4, 4))
    game.move(KlondikeMove(Position.Column5, Position.Foundation1, 1))
    game.move(KlondikeMove(Position.Column3, Position.Column6, 2))

    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))
    game.move(KlondikeMove(Position.Stock, Position.Waste, 1))

    game.move(KlondikeMove(Position.Foundation1, Position.Column7, 1))

    game.move(KlondikeMove(Position.Column7, Position.Foundation2, 1))


    game.draw_layout_console()

    
    # Gameloop for user input to test moves
    # while the user has not entered 'e' to exit or 'exit' to exit
    # clear the console 
    # diplays the currrent layout
    # prompt the user to enter a move in the format 'source destination num_cards' e.g. 'C1 C3 2' to move 2 cards from column 1 to column 3
    # source and destination can be C1 to C7 for columns, F1 to F4 for foundations, S for stock, W for waste
    exit = False
    while not exit:
        os.system('cls' if os.name == 'nt' else 'clear')
        game.draw_layout_console()
        user_input = input("Enter move (e to exit) in format 'source destination num_cards': ")
        if user_input.lower() == 'e' or user_input.lower() == 'exit':
            exit = True
            continue
        try:
            source_str, dest_str, num_cards_str = user_input.split()

            print(source_str)
            source = parse_position(source_str)
            destination = parse_position(dest_str)
            num_cards = int(num_cards_str)
            if source is None or destination is None:
                print(f"source: {source}, destination: {destination}")
                print("Invalid source or destination. Please use C1-C7 for columns, F1-F4 for foundations, S for stock, W for waste.")
                input("Press Enter to continue...")
                continue
            move = KlondikeMove(source, destination, num_cards)
            if game.move(move):
                print("Move executed.")
            else:
                print("Move is invalid.")
        except Exception as e:
            print(f"Error processing move: {e}")
        input("Press Enter to continue...")



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
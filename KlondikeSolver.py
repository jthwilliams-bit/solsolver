from KlondikeGame import KlondikeGame
from KlondikeMove import KlondikeMove, Position
from card import Card
import hashlib



class KlondikeSolver:
    debug = False
    
    def __init__(self, game: KlondikeGame):
        self.game = game
        self.moves = []
        self.solved = False 


    


    # For the given board state, 
    #   - check if this board is one that we've already seen,  if it is, return a None 
    #   - check if it is a win state
    #   - find all possible legal moves
    # check the new board state to see if it matches a previously seen state
    # if not, add it to the list of seen states and continue searching
    def solve(self):
        self.states_seen = []
        index = 0
        while not self.solved:

            pass
    
    def can_move_to_foundation(self, card, foundation_index):
        if self.debug: print(f"Checking move of {card} to foundation {foundation_index+1}")
        foundation = self.game.foundation[foundation_index]
        if not foundation:
            return card.rank == 'A'
        top_card = foundation[-1]
        return (card.suit == top_card.suit) and (Card.RANKS.index(card.rank) == (Card.RANKS.index(top_card.rank) + 1)%13)
    def can_move_to_tableau(self, card, tableau_index):
        tableau = self.game.tableau_face_up [tableau_index]
        if not tableau:
            return card.rank == 'K'
        top_card = tableau[-1]
        return (card.color != top_card.color) and (Card.RANKS.index(card.rank) == (Card.RANKS.index(top_card.rank) - 1))

    def getallpossiblemove(self):
        possible_moves = []

        # Moves from waste to foundation
        if self.game.waste:
            top_waste = self.game.waste[-1]
            for i in range(4):
                if self.can_move_to_foundation(top_waste, i):
                    possible_moves.append(KlondikeMove(Position.Waste, Position(f"f{i+1}")))

        # Moves from waste to tableau
        if self.game.waste:
            top_waste = self.game.waste[-1]
            for i in range(7):
                if self.can_move_to_tableau(top_waste, i):
                    possible_moves.append(KlondikeMove(Position.Waste, Position(f"c{i+1}")))

        # Moves from tableau to foundation
        for i in range(7):
            if self.game.tableau[i]:
                top_tableau = self.game.tableau_face_up[i][-1]
                for j in range(4):
                    if self.can_move_to_foundation(top_tableau, j):
                        possible_moves.append(KlondikeMove(Position(f"c{i+1}"), Position(f"f{j+1}")))

        # Moves from tableau to tableau
        for i in range(7):
            for j in range(7):
                if i != j and self.game.tableau[i]:
                    for k in range(len(self.game.tableau_face_up[i])):
                        moving_card = self.game.tableau_face_up[i][k]
                        if self.can_move_to_tableau(moving_card, j):
                            possible_moves.append(KlondikeMove(Position(f"c{i+1}"), Position(f"c{j+1}"), len(self.game.tableau[i]) - k))
                            break  # Only need the first valid move

        # Moves from foundation to tableau (if allowed)
        for i in range(4):
            if self.game.foundation[i]:
                top_foundation = self.game.foundation[i][-1]
                for j in range(7):
                    if self.can_move_to_tableau(top_foundation, j):
                        possible_moves.append(KlondikeMove(Position(f"f{i+1}"), Position(f"c{j+1}")))

        return possible_moves


if __name__ == "__main__":
    game = KlondikeGame(seed=2256)
    game.deal()

    print(game.hashmd5())

    solver = KlondikeSolver(game)

    game.draw_layout_console()

    moves = solver.getallpossiblemove()
    for move in moves:
        print(move)

    print("Initialized Klondike Solver")

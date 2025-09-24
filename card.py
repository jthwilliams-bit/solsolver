import json

# Card class for representing a playing card
class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    COLOR = {'Hearts': 'Red', 'Diamonds': 'Red', 'Clubs': 'Black', 'Spades': 'Black'}

    def __init__(self, suit, rank):
        if suit not in Card.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        if rank not in Card.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        self.suit = suit
        self.rank = rank
        self.color = Card.COLOR[suit]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    def to_dict(self):
        return {'suit': self.suit, 'rank': self.rank, 'color': self.color}

    @staticmethod
    def from_dict(data):
        card = Card(data['suit'], data['rank'])
        card.color = data['color']
        return card
    
    def to_json(self):
        return json.dumps(self.to_dict())
    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Card.from_dict(data)
    

# --- IGNORE ---
# Example usage:
# card = Card('Hearts', 'A')
# print(card)  # Output: A of Hearts


if __name__ == "__main__":
    card = Card('Hearts', 'A')
    print(card)  # Output: A of Hearts
    json_str = card.to_json()
    print(json_str)  # JSON representation
    new_card = Card.from_json(json_str)
    print(new_card)  # Output: A of Hearts
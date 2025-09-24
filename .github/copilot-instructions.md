# Copilot Instructions for SolSolver

This is a solitaire solver project focused on Klondike solitaire game mechanics.

## Architecture Overview

- **`card.py`**: Core `Card` class with suit/rank/color system and JSON serialization
- **`deckbuiler.py`**: `DeckBuilder` creates standard 52-card decks with shuffling
- **`Layout.json`**: Game state representation for Klondike solitaire layouts

## Key Patterns & Conventions

### Card Representation
The project uses two different card value systems that need alignment:
- **Python Card class**: Uses ranks `['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']`
- **Layout.json format**: Uses values like `"1"`, `"10"`, `"A"`, `"K"`, `"Q"` (inconsistent with Card class)

### JSON Game State Structure
`Layout.json` follows this specific schema:
```json
{
  "Properties": {"Type": "Klondike", "Sead": "12345", "Moves": 5, "Waste": 3},
  "Cards": {
    "Home": {"1": [], "2": [], "3": [], "4": []},
    "Columns": {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": []},
    "Stock": [],
    "Waste": []
  },
  "Moves": []
}
```

### Card JSON Format in Layouts
Cards in layouts use: `{"Color": "Red|Black", "Suit": "Hearts|Diamonds|Clubs|Spades", "Value": "A|K|Q|J|10|9|8|7|6|5|4|3|2", "FaceUp": true|false}`

## Critical Issues to Address
1. **Value Mismatch**: Card class uses "rank" property but Layout.json expects "Value"
2. **Numbering Inconsistency**: Card class has no "1" rank, but Layout.json shows `"Value": "1"`
3. **Missing FaceUp**: Card class doesn't track face-up/face-down state needed for solitaire

## Development Workflows
- Run individual modules: `python card.py` or `python deckbuiler.py` 
- Card class supports JSON round-trip: `card.to_json()` → `Card.from_json()`
- Note: "deckbuiler.py" has a typo in filename (should be "deckbuilder")

## Integration Points
When working between Card objects and Layout.json:
- Convert Card.rank to Layout "Value" format
- Handle face-up/face-down state for tableau cards
- Map between 1-indexed Layout columns and 0-indexed arrays
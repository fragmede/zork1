# Zork I - Python Edition

A Python conversion of the classic 1980 interactive fiction game Zork I, originally created by Infocom.

## About

This project is a faithful conversion of Zork I from ZIL (Zork Implementation Language) to Python. The original game was written by Marc Blank, Dave Lebling, Bruce Daniels, and Tim Anderson.

This Python version aims to:
- Preserve the original gameplay and text
- Make the code more accessible and understandable
- Enable easier modification and extension
- Provide an educational resource for game development

## Status

**Current Phase: Foundation (Phase 1)**

✅ **Completed:**
- Project structure setup
- Base GameObject class
- Room, Item, Container, and Actor classes
- ObjectFlag system (IntFlag enums)
- Output formatting utilities
- Basic demo system

🚧 **In Progress:**
- Parser implementation
- Game engine and main loop
- World data conversion

📋 **Planned:**
- Complete world data (all rooms, items, NPCs)
- All verb implementations
- Clock/daemon system
- Save/restore functionality
- Full game testing

## Installation

```bash
# Clone the repository
cd zork1_python

# No external dependencies required for core game!
# Optional: Install development dependencies
pip install -r requirements.txt
```

## Running

```bash
# Run the foundation demo
python main.py
```

## Project Structure

```
zork1_python/
├── core/           # Game engine, state management, clock system
├── parser/         # Lexer, parser, grammar, vocabulary
├── objects/        # GameObject, Room, Item, Actor, Container classes
├── world_data/     # Room definitions, item data, NPC data
├── actions/        # Verb handlers and action dispatchers
├── utils/          # Output, flags, helper functions
├── tests/          # Unit and integration tests
└── main.py         # Entry point
```

## Architecture

The conversion follows these design principles:

1. **Object-Oriented Design**: ZIL objects → Python classes
2. **Clear Separation**: Parser, game engine, and world data are separate
3. **Type Safety**: Using Python type hints and enums
4. **Testability**: Comprehensive test coverage
5. **Readability**: Clear, documented code

### Core Components

- **GameObject**: Base class for all game entities
- **Room**: Locations with exits and descriptions
- **Item**: Objects that can be manipulated
- **Container**: Objects that hold other objects
- **Actor**: NPCs with AI and inventory
- **Parser**: Natural language command parsing (TODO)
- **GameEngine**: Main loop and action execution (TODO)

## Development

### Running Tests

```bash
pytest tests/
pytest --cov=. tests/  # With coverage
```

### Code Style

This project follows PEP 8 style guidelines.

```bash
# Format code
black .

# Lint code
flake8 .
pylint zork1_python/
```

## Credits

**Original Game:**
- Marc Blank
- Dave Lebling
- Bruce Daniels
- Tim Anderson
- Infocom (1980)

**Python Conversion:**
- Based on the ZIL source code released by Infocom
- Conversion plan and implementation (2024)

## License

The original Zork I source code has been released by Activision.
This Python conversion is provided for educational and historical preservation purposes.

## References

- [Original ZIL Source Code](../)
- [Conversion Plan](../plan.md)
- [ZILF Compiler](http://zilf.io)
- [Interactive Fiction Database](https://ifdb.tads.org/viewgame?id=0dbnusxunq7fw5ro)

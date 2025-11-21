# COMPREHENSIVE ZORK I TO PYTHON CONVERSION PLAN

## PART 1: UNDERSTANDING THE SOURCE

### 1.1 ZIL Language Characteristics

ZIL (Zork Implementation Language) is a dialect of MDL/Muddle (a Lisp variant) with these key features:
- **Syntax**: Uses `<>` angle brackets instead of `()` parentheses
- **Evaluation**: Prefix notation (operator-first)
- **Data Types**: Atoms, strings, numbers, tables (arrays), objects
- **Macros**: Compile-time code generation (DEFMAC)
- **Type System**: Optional type declarations (#DECL)
- **Memory Model**: Z-Machine byte/word oriented storage

### 1.2 Core System Components Identified

From analyzing the codebase, I found these major subsystems:

| File | Purpose | Lines (approx) | Complexity |
|------|---------|----------------|------------|
| `zork1.zil` | Main entry, file includes | 34 | Low |
| `gmain.zil` | Game loop, action dispatcher | ~1500 | High |
| `gparser.zil` | Natural language parser | ~3000 | Very High |
| `gsyntax.zil` | Grammar/syntax definitions | ~1000 | Medium |
| `gverbs.zil` | Verb implementations | ~1200 | Medium |
| `gglobals.zil` | Global objects/variables | ~800 | Low |
| `gmacros.zil` | Macro definitions | ~400 | Medium |
| `gclock.zil` | Timing/interrupt system | ~200 | Medium |
| `1dungeon.zil` | Rooms, objects, world data | ~3000 | Medium |
| `1actions.zil` | Object-specific actions | ~2000 | Medium-High |

---

## PART 2: PYTHON ARCHITECTURE DESIGN

### 2.1 Proposed Python Project Structure

```
zork1_python/
├── core/
│   ├── __init__.py
│   ├── game_engine.py      # Main game loop (gmain.zil)
│   ├── world.py            # World state management
│   ├── clock.py            # Timing/daemon system (gclock.zil)
│   └── constants.py        # Global constants
├── parser/
│   ├── __init__.py
│   ├── lexer.py           # Tokenization
│   ├── parser.py          # Command parsing (gparser.zil)
│   ├── grammar.py         # Syntax definitions (gsyntax.zil)
│   └── vocabulary.py      # Word lists, synonyms
├── objects/
│   ├── __init__.py
│   ├── base.py            # Base GameObject class
│   ├── room.py            # Room class
│   ├── item.py            # Item class
│   ├── actor.py           # NPC/Actor class
│   └── container.py       # Container objects
├── world_data/
│   ├── __init__.py
│   ├── rooms.py           # Room definitions (1dungeon.zil)
│   ├── items.py           # Item definitions
│   ├── npcs.py            # NPC definitions
│   └── globals.py         # Global objects (gglobals.zil)
├── actions/
│   ├── __init__.py
│   ├── verbs.py           # Verb handlers (gverbs.zil)
│   ├── handlers.py        # Action dispatchers
│   └── item_actions.py    # Item-specific actions (1actions.zil)
├── utils/
│   ├── __init__.py
│   ├── output.py          # Text output formatting
│   ├── flags.py           # Flag/bit manipulation
│   └── helpers.py         # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_objects.py
│   └── test_game_logic.py
├── main.py                # Entry point
├── requirements.txt
└── README.md
```

### 2.2 Core Design Patterns

**Object-Oriented Design:**
- **GameObject Base Class**: All rooms, items, NPCs inherit from this
- **Flags as Enums**: Convert ZIL FLAGS to Python Enums/IntFlags
- **Properties as Attributes**: ZIL properties become Python class attributes
- **Actions as Methods**: Object action functions become instance methods

**Parser Design:**
- **Lexer-Parser separation**: Two-phase parsing like ZIL
- **Grammar as Data**: Define syntax rules in declarative format (YAML/JSON or Python data structures)
- **Command Pattern**: Each parsed command becomes a Command object

**State Management:**
- **World State Singleton**: Global game state (current room, inventory, etc.)
- **Event Queue**: For clock/daemon system
- **Save/Restore**: Pickle or JSON serialization

---

## PART 3: DATA STRUCTURE CONVERSION STRATEGY

### 3.1 ZIL OBJECT → Python Class

**ZIL Example:**
```zil
<OBJECT SKULL
    (IN LAND-OF-LIVING-DEAD)
    (SYNONYM SKULL HEAD TREASURE)
    (ADJECTIVE CRYSTAL)
    (DESC "crystal skull")
    (FDESC "Lying in one corner of the room is a beautifully
            carved crystal skull. It appears to be grinning
            at you rather nastily.")
    (FLAGS TAKEBIT)
    (VALUE 10)
    (TVALUE 10)>
```

**Python Translation:**
```python
class CrystalSkull(Item):
    def __init__(self):
        super().__init__(
            id="SKULL",
            location="LAND-OF-LIVING-DEAD",
            synonyms=["skull", "head", "treasure"],
            adjectives=["crystal"],
            short_desc="crystal skull",
            long_desc="""Lying in one corner of the room is a beautifully
                         carved crystal skull. It appears to be grinning
                         at you rather nastily.""",
            flags={ObjectFlag.TAKEABLE},
            value=10,
            treasure_value=10
        )
```

**Alternative: Data-Driven Approach:**
```python
# items.yaml
SKULL:
  class: Item
  location: LAND_OF_LIVING_DEAD
  synonyms: [skull, head, treasure]
  adjectives: [crystal]
  short_desc: crystal skull
  long_desc: |
    Lying in one corner of the room is a beautifully
    carved crystal skull. It appears to be grinning
    at you rather nastily.
  flags: [TAKEABLE]
  value: 10
  treasure_value: 10
```

### 3.2 ZIL ROUTINE → Python Function/Method

**ZIL Example:**
```zil
<ROUTINE BOARD-F ()
    <COND (<VERB? TAKE EXAMINE>
           <TELL "The boards are securely fastened." CR>)>>
```

**Python Translation:**
```python
def board_action(self, verb, direct_obj, indirect_obj):
    """Action handler for BOARD object."""
    if verb in [Verb.TAKE, Verb.EXAMINE]:
        output.tell("The boards are securely fastened.")
        return ActionResult.HANDLED
    return ActionResult.NOT_HANDLED
```

### 3.3 ZIL FLAGS → Python IntFlag Enum

**ZIL:**
```zil
(FLAGS RMUNGBIT INVISIBLE TOUCHBIT SURFACEBIT TRYTAKEBIT
       OPENBIT SEARCHBIT TRANSBIT ONBIT RLANDBIT FIGHTBIT
       STAGGERED WEARBIT)
```

**Python:**
```python
from enum import IntFlag, auto

class ObjectFlag(IntFlag):
    RMUNG = auto()
    INVISIBLE = auto()
    TOUCH = auto()
    SURFACE = auto()
    TRY_TAKE = auto()
    OPEN = auto()
    SEARCHABLE = auto()
    TRANSPARENT = auto()
    ON = auto()
    RLAND = auto()
    FIGHTABLE = auto()
    STAGGERED = auto()
    WEARABLE = auto()
    TAKEABLE = auto()
    # ... etc
```

### 3.4 ZIL GLOBALS → Python Module Globals or Singleton

**Approach 1: Module-level globals**
```python
# world_state.py
player = None
current_room = None
moves = 0
score = 0
verbose = False
super_brief = False
```

**Approach 2: State class (preferred)**
```python
class GameState:
    """Singleton game state."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.player = None
        self.current_room = None
        self.moves = 0
        self.score = 0
        self.verbose = False
        self.super_brief = False
        self.inventory = []
        self.clock_events = []
```

### 3.5 ZIL Tables → Python Lists/Dicts

**ZIL:**
```zil
<GLOBAL P-ITBL <TABLE 0 0 0 0 0 0 0 0 0 0>>
```

**Python:**
```python
# Simple list
p_itbl = [0] * 10

# Or named tuple for clarity
from collections import namedtuple
ParseInfo = namedtuple('ParseInfo', [
    'verb', 'verbn', 'prep1', 'prep1n',
    'prep2', 'prep2n', 'nc1', 'nc1l', 'nc2', 'nc2l'
])
```

---

## PART 4: PARSER IMPLEMENTATION STRATEGY

The parser is the most complex component (~3000 lines). Here's the conversion strategy:

### 4.1 Parser Architecture

**Three-Phase Parsing:**

1. **Lexical Analysis (Tokenization)**
   - Split input into words
   - Look up words in vocabulary
   - Handle synonyms and abbreviations
   - Create token stream

2. **Syntactic Analysis (Parsing)**
   - Match token stream against grammar rules
   - Identify: VERB + DIRECT_OBJECT + PREPOSITION + INDIRECT_OBJECT
   - Handle multiple objects ("take all", "drop sword and lamp")
   - Resolve pronouns ("it", "them", "him", "her")

3. **Semantic Analysis (Object Resolution)**
   - Find objects matching descriptions
   - Check object visibility/accessibility
   - Disambiguate ("which lamp: the brass lamp or the lantern?")
   - Validate action legality

### 4.2 Lexer Implementation

```python
class Lexer:
    """Tokenizes player input."""

    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        self.break_chars = ".,\""

    def tokenize(self, input_text):
        """Convert input string to list of tokens."""
        # 1. Normalize: lowercase, strip extra spaces
        text = input_text.lower().strip()

        # 2. Split on whitespace and punctuation
        words = self._split_with_breaks(text)

        # 3. Look up each word in vocabulary
        tokens = []
        for word in words:
            token = self._lookup_word(word)
            if token:
                tokens.append(token)
            else:
                tokens.append(Token(word, TokenType.UNKNOWN))

        return tokens

    def _lookup_word(self, word):
        """Find word in vocabulary, handling synonyms."""
        # Check if it's a verb
        if word in self.vocabulary.verbs:
            return Token(word, TokenType.VERB,
                        canonical=self.vocabulary.verbs[word])

        # Check if it's a direction
        if word in self.vocabulary.directions:
            return Token(word, TokenType.DIRECTION,
                        canonical=self.vocabulary.directions[word])

        # Check if it's a noun/adjective
        if word in self.vocabulary.nouns:
            return Token(word, TokenType.NOUN,
                        canonical=self.vocabulary.nouns[word])

        if word in self.vocabulary.adjectives:
            return Token(word, TokenType.ADJECTIVE,
                        canonical=self.vocabulary.adjectives[word])

        # Check if it's a preposition
        if word in self.vocabulary.prepositions:
            return Token(word, TokenType.PREPOSITION,
                        canonical=self.vocabulary.prepositions[word])

        # Check if it's a buzz word (ignored)
        if word in self.vocabulary.buzzwords:
            return None  # Filtered out

        return None  # Unknown word
```

### 4.3 Grammar Definition

**ZIL Syntax Example:**
```zil
<SYNTAX ATTACK OBJECT (FIND ACTORBIT) (ON-GROUND IN-ROOM)
        WITH OBJECT (FIND WEAPONBIT) (HELD CARRIED HAVE)
        = V-ATTACK>
```

**Python Grammar Structure:**
```python
class SyntaxRule:
    """Represents a command syntax pattern."""
    def __init__(self, verb, pattern, handler, constraints=None):
        self.verb = verb
        self.pattern = pattern  # e.g., "VERB OBJECT [WITH OBJECT]"
        self.handler = handler
        self.constraints = constraints or {}

# Grammar definitions
GRAMMAR = [
    # ATTACK <actor> WITH <weapon>
    SyntaxRule(
        verb="ATTACK",
        pattern=["VERB", "OBJECT", "WITH", "OBJECT"],
        handler=verbs.v_attack,
        constraints={
            "direct_object": {
                "find_flags": [ObjectFlag.ACTOR],
                "location": ["ON_GROUND", "IN_ROOM"]
            },
            "indirect_object": {
                "find_flags": [ObjectFlag.WEAPON],
                "location": ["HELD", "CARRIED", "HAVE"]
            }
        }
    ),

    # TAKE <object>
    SyntaxRule(
        verb="TAKE",
        pattern=["VERB", "OBJECT"],
        handler=verbs.v_take,
        constraints={
            "direct_object": {
                "find_flags": [ObjectFlag.TAKEABLE],
                "location": ["ON_GROUND", "IN_ROOM", "IN_CONTAINER"]
            }
        }
    ),

    # ... hundreds more rules
]
```

### 4.4 Parser Implementation

```python
class Parser:
    """Parses tokenized commands into executable actions."""

    def __init__(self, grammar, world):
        self.grammar = grammar
        self.world = world
        self.last_object = None  # For pronoun resolution

    def parse(self, tokens):
        """Parse token list into ParsedCommand."""
        # 1. Extract verb
        verb_token = self._find_verb(tokens)
        if not verb_token:
            return ParseResult(error="I don't understand that verb.")

        # 2. Find matching syntax rule
        for rule in self.grammar.get_rules(verb_token.canonical):
            match = self._try_match_rule(tokens, rule)
            if match:
                return match

        return ParseResult(error=f"I don't know how to {verb_token.word} like that.")

    def _try_match_rule(self, tokens, rule):
        """Try to match tokens against a syntax rule."""
        # Extract noun phrases
        direct_np = self._extract_noun_phrase(tokens, after_verb=True)
        indirect_np = None

        # Look for preposition
        prep_idx = self._find_preposition(tokens)
        if prep_idx:
            indirect_np = self._extract_noun_phrase(
                tokens, start=prep_idx + 1
            )

        # Resolve to actual objects
        direct_objs = self._resolve_objects(
            direct_np,
            rule.constraints.get("direct_object")
        )

        indirect_objs = []
        if indirect_np:
            indirect_objs = self._resolve_objects(
                indirect_np,
                rule.constraints.get("indirect_object")
            )

        # Handle disambiguation
        if len(direct_objs) > 1:
            direct_objs = self._disambiguate(direct_objs, direct_np)

        if direct_objs:
            return ParsedCommand(
                verb=rule.verb,
                direct_object=direct_objs[0],
                indirect_object=indirect_objs[0] if indirect_objs else None,
                handler=rule.handler
            )

        return None

    def _resolve_objects(self, noun_phrase, constraints):
        """Find objects matching noun phrase."""
        candidates = []

        # Get visible objects
        visible = self.world.get_visible_objects()

        for obj in visible:
            # Check if noun matches
            if noun_phrase.noun not in obj.synonyms:
                continue

            # Check if adjectives match
            if noun_phrase.adjectives:
                if not all(adj in obj.adjectives
                          for adj in noun_phrase.adjectives):
                    continue

            # Check constraints (flags, location)
            if constraints:
                if not self._check_constraints(obj, constraints):
                    continue

            candidates.append(obj)

        return candidates
```

---

## PART 5: GAME LOOP & EXECUTION MODEL

### 5.1 Main Game Loop

**ZIL Original (gmain.zil:34-36):**
```zil
<ROUTINE MAIN-LOOP ("AUX" TRASH)
    <REPEAT ()
        <SET TRASH <MAIN-LOOP-1>>>>
```

**Python Translation:**
```python
class GameEngine:
    """Main game engine orchestrator."""

    def __init__(self):
        self.state = GameState()
        self.parser = Parser(GRAMMAR, self.state.world)
        self.clock = ClockSystem()
        self.output = OutputManager()
        self.running = True

    def main_loop(self):
        """Primary game loop - runs indefinitely."""
        self._initialize_game()

        while self.running:
            try:
                self._main_loop_iteration()
            except GameOver as e:
                self._handle_game_over(e)
                break
            except QuitGame:
                break
            except Exception as e:
                self._handle_error(e)

    def _main_loop_iteration(self):
        """Single iteration of game loop."""
        # 1. Display prompt
        self.output.prompt()

        # 2. Get player input
        user_input = input("> ")

        # 3. Tokenize input
        tokens = self.parser.lexer.tokenize(user_input)

        # 4. Parse into command
        parsed = self.parser.parse(tokens)

        if parsed.error:
            self.output.tell(parsed.error)
            return

        # 5. Execute command
        self._execute_command(parsed)

        # 6. Run clock/daemon system
        self.clock.tick()

        # 7. Check win/lose conditions
        self._check_end_conditions()
```

### 5.2 Action Execution System

**Command Execution Flow:**
```
User Input → Lexer → Parser → Command → Pre-Action → Action → Post-Action → Clock
```

**Implementation:**
```python
def _execute_command(self, command):
    """Execute a parsed command."""
    # 1. Pre-action checks (global handlers)
    result = self._run_pre_actions(command)
    if result.stop_processing:
        return result

    # 2. Object-specific action
    if command.direct_object and hasattr(command.direct_object, 'action'):
        result = command.direct_object.action(
            command.verb,
            command.direct_object,
            command.indirect_object
        )
        if result.handled:
            return result

    # 3. Default verb handler
    result = command.handler(
        command.direct_object,
        command.indirect_object
    )

    # 4. Post-action processing
    self._run_post_actions(command, result)

    # 5. Update "IT" reference for pronouns
    if command.direct_object:
        self.parser.last_object = command.direct_object

    return result
```

### 5.3 Clock/Daemon System

**ZIL Original (gclock.zil):**
```zil
<ROUTINE CLOCKER ("AUX" C E TICK (FLG <>))
    <SET C <REST ,C-TABLE <COND (,P-WON ,C-INTS) (T ,C-DEMONS)>>>
    <SET E <REST ,C-TABLE ,C-TABLELEN>>
    <REPEAT ()
        <COND (<==? .C .E>
               <SETG MOVES <+ ,MOVES 1>>
               <RETURN .FLG>)
              ...
```

**Python Translation:**
```python
class ClockSystem:
    """Manages scheduled events and interrupts (daemons/interrupts)."""

    def __init__(self):
        self.events = []  # List of ScheduledEvent
        self.demons = []  # Always-running events
        self.interrupts = []  # Conditional events

    def queue(self, callback, ticks, is_demon=False):
        """Schedule an event to run after N ticks."""
        event = ScheduledEvent(
            callback=callback,
            ticks_remaining=ticks,
            enabled=True,
            is_demon=is_demon
        )

        if is_demon:
            self.demons.append(event)
        else:
            self.interrupts.append(event)

        return event

    def tick(self):
        """Run one clock tick - called after each command."""
        # Determine which events to process
        events = self.demons if game_state.player_won else self.interrupts

        any_triggered = False

        for event in events:
            if not event.enabled:
                continue

            if event.ticks_remaining > 0:
                event.ticks_remaining -= 1

            if event.ticks_remaining == 0:
                # Fire the event
                result = event.callback()
                any_triggered = True

                # Reset if it's recurring
                if event.recurring:
                    event.ticks_remaining = event.interval
                else:
                    event.enabled = False

        # Increment global move counter
        game_state.moves += 1

        return any_triggered

class ScheduledEvent:
    """Represents a scheduled event."""
    def __init__(self, callback, ticks_remaining, enabled=True,
                 is_demon=False, recurring=False, interval=0):
        self.callback = callback
        self.ticks_remaining = ticks_remaining
        self.enabled = enabled
        self.is_demon = is_demon
        self.recurring = recurring
        self.interval = interval

# Usage example:
def thief_moves():
    """Daemon that moves the thief around."""
    if random.random() < 0.3:
        new_room = random.choice(thief.reachable_rooms())
        thief.move_to(new_room)
        if new_room == game_state.current_room:
            output.tell("A seedy-looking individual appears.")

# Schedule it
clock.queue(thief_moves, ticks=5, is_demon=True, recurring=True, interval=5)
```

---

## PART 6: SPECIFIC CONVERSION CHALLENGES & SOLUTIONS

### 6.1 Challenge: ZIL Macros

**Problem:** ZIL uses compile-time macros (DEFMAC) that don't have direct Python equivalents.

**Solution Options:**

1. **Expand macros during conversion** - Pre-process ZIL, expand all macros to their full form
2. **Convert to Python functions** - Simple macros → functions
3. **Use Python decorators** - For pattern-like macros

**Example - TELL Macro:**

ZIL:
```zil
<TELL "You are in a " D ,HERE CR>
```

Python:
```python
# Option 1: Helper function
tell(f"You are in a {state.current_room.description}")

# Option 2: Custom function
def tell(*args):
    """TELL macro replacement."""
    output = []
    i = 0
    while i < len(args):
        if args[i] == 'D':  # Description
            output.append(args[i+1].short_desc)
            i += 2
        elif args[i] == 'CR':  # Carriage return
            output.append('\n')
            i += 1
        else:
            output.append(str(args[i]))
            i += 1
    print(''.join(output), end='')
```

### 6.2 Challenge: Dynamic Object Location (IN)

**Problem:** ZIL objects can be inside other objects, forming a containment hierarchy.

**Solution:**
```python
class GameObject:
    """Base class for all game objects."""

    def __init__(self, id, location=None):
        self.id = id
        self._location = location
        self.contents = []

        if location:
            self.move_to(location)

    @property
    def location(self):
        """Current container/room."""
        return self._location

    def move_to(self, new_location):
        """Move this object to a new location."""
        # Remove from old location
        if self._location:
            if isinstance(self._location, str):
                # Resolve string ID to object
                self._location = world.get_object(self._location)
            self._location.contents.remove(self)

        # Add to new location
        if new_location:
            if isinstance(new_location, str):
                new_location = world.get_object(new_location)
            new_location.contents.append(self)
            self._location = new_location
        else:
            self._location = None

    def is_in(self, container):
        """Check if this object is in a container."""
        return self._location == container

    def is_accessible(self):
        """Check if object is accessible to player."""
        # Object must be:
        # 1. In current room
        # 2. In player's inventory
        # 3. In an open container in current room/inventory

        if self.location == game_state.current_room:
            return True

        if self.location == game_state.player:
            return True

        # Check containers recursively
        container = self.location
        while container:
            if container == game_state.current_room or \
               container == game_state.player:
                # Check if all containers in chain are open/transparent
                return self._all_containers_open()
            container = container.location

        return False
```

### 6.3 Challenge: Bit Flags

**Problem:** ZIL uses bit flags extensively for object properties.

**Solution:**
```python
from enum import IntFlag, auto

class ObjectFlag(IntFlag):
    """Object property flags."""
    INVISIBLE = auto()
    TOUCHABLE = auto()
    SURFACE = auto()
    TAKEABLE = auto()
    OPENABLE = auto()
    OPEN = auto()
    SEARCHABLE = auto()
    TRANSPARENT = auto()
    ON = auto()
    WEARABLE = auto()
    CONTAINER = auto()
    ACTOR = auto()
    WEAPON = auto()
    # ... many more

class GameObject:
    def __init__(self, flags=None):
        self.flags = flags or ObjectFlag(0)

    def has_flag(self, flag):
        """Check if object has a flag."""
        return bool(self.flags & flag)

    def set_flag(self, flag):
        """Set a flag."""
        self.flags |= flag

    def clear_flag(self, flag):
        """Clear a flag."""
        self.flags &= ~flag

    @property
    def is_takeable(self):
        return self.has_flag(ObjectFlag.TAKEABLE)

    @property
    def is_open(self):
        return self.has_flag(ObjectFlag.OPEN)

    def open(self):
        if self.has_flag(ObjectFlag.OPENABLE):
            self.set_flag(ObjectFlag.OPEN)
            return True
        return False
```

### 6.4 Challenge: COND (Multi-way Conditional)

**Problem:** ZIL's COND is like Lisp's cond, not like Python's if.

**ZIL:**
```zil
<COND (<VERB? TAKE>
       <TELL "You take it." CR>)
      (<VERB? DROP>
       <TELL "You drop it." CR>)
      (T
       <TELL "You can't do that." CR>)>
```

**Python:**
```python
# Option 1: if-elif-else chain
if verb == Verb.TAKE:
    tell("You take it.")
elif verb == Verb.DROP:
    tell("You drop it.")
else:
    tell("You can't do that.")

# Option 2: Match statement (Python 3.10+)
match verb:
    case Verb.TAKE:
        tell("You take it.")
    case Verb.DROP:
        tell("You drop it.")
    case _:
        tell("You can't do that.")

# Option 3: Dictionary dispatch
actions = {
    Verb.TAKE: lambda: tell("You take it."),
    Verb.DROP: lambda: tell("You drop it."),
}
actions.get(verb, lambda: tell("You can't do that."))()
```

---

## PART 7: CONVERSION WORKFLOW & IMPLEMENTATION PHASES

### 7.1 Conversion Approach: Manual vs Automated

**Recommended: Hybrid Approach**

1. **Automated ZIL Parser (30% effort, 60% coverage)**
   - Build a ZIL AST parser to extract structure
   - Auto-generate Python scaffolding
   - Extract all object definitions automatically
   - Extract constants and globals

2. **Manual Translation (70% effort, 40% coverage but critical)**
   - Hand-convert complex routines
   - Implement parser logic
   - Implement game-specific action handlers
   - Test and debug

### 7.2 Implementation Phases

**PHASE 1: Foundation (Week 1-2)**
- [ ] Set up Python project structure
- [ ] Create base classes (GameObject, Room, Item, Actor)
- [ ] Implement flag system (IntFlag enums)
- [ ] Create output/formatting utilities
- [ ] Set up test framework

**PHASE 2: Data Conversion (Week 2-3)**
- [ ] Build ZIL object parser (or manual extraction)
- [ ] Convert all room definitions (1dungeon.zil → rooms.py)
- [ ] Convert all item definitions (1dungeon.zil → items.py)
- [ ] Convert all global objects (gglobals.zil → globals.py)
- [ ] Create world initialization

**PHASE 3: Core Engine (Week 3-4)**
- [ ] Implement game state management
- [ ] Create basic game loop
- [ ] Implement clock/daemon system (gclock.zil → clock.py)
- [ ] Implement save/restore functionality
- [ ] Basic input/output

**PHASE 4: Parser (Week 4-6)** ⚠️ MOST COMPLEX
- [ ] Build vocabulary system
- [ ] Implement lexer/tokenizer
- [ ] Convert syntax definitions (gsyntax.zil → grammar.py)
- [ ] Implement core parser logic (gparser.zil → parser.py)
- [ ] Implement object resolution
- [ ] Handle pronouns, "all", multiple objects
- [ ] Test extensively with various inputs

**PHASE 5: Verbs & Actions (Week 6-7)**
- [ ] Convert basic verbs (gverbs.zil → verbs.py)
  - TAKE, DROP, INVENTORY, LOOK, EXAMINE
  - OPEN, CLOSE, LOCK, UNLOCK
  - GO, WALK, CLIMB
  - SAVE, RESTORE, QUIT, RESTART
- [ ] Implement action dispatch system
- [ ] Convert object-specific actions (1actions.zil → item_actions.py)

**PHASE 6: Game Logic (Week 7-8)**
- [ ] Implement scoring system
- [ ] Implement death/resurrection
- [ ] Implement lighting model (darkness, light sources)
- [ ] Implement combat system (if needed)
- [ ] Convert all room action handlers
- [ ] Convert all item action handlers

**PHASE 7: Testing & Polish (Week 8-10)**
- [ ] Playtest entire game
- [ ] Fix bugs
- [ ] Compare output with original game
- [ ] Performance optimization
- [ ] Documentation

### 7.3 Suggested Conversion Tools

**Tool 1: ZIL AST Parser**
```python
# zil_parser.py - Parse ZIL source into Python AST

import re
from typing import List, Dict, Any

class ZILParser:
    """Parse ZIL source files into Python-friendly structures."""

    def parse_file(self, filename):
        """Parse a .zil file."""
        with open(filename, 'r') as f:
            content = f.read()

        # Remove comments
        content = re.sub(r';.*?$', '', content, flags=re.MULTILINE)

        # Find all top-level forms
        forms = self._extract_forms(content)

        return {
            'objects': [f for f in forms if f['type'] == 'OBJECT'],
            'routines': [f for f in forms if f['type'] == 'ROUTINE'],
            'globals': [f for f in forms if f['type'] == 'GLOBAL'],
            'constants': [f for f in forms if f['type'] == 'CONSTANT'],
            'syntax': [f for f in forms if f['type'] == 'SYNTAX'],
        }

    def _extract_forms(self, content):
        """Extract all <FORM ...> structures."""
        forms = []
        i = 0
        while i < len(content):
            if content[i] == '<':
                form, end = self._parse_form(content, i)
                if form:
                    forms.append(form)
                    i = end
                else:
                    i += 1
            else:
                i += 1
        return forms

    def _parse_form(self, content, start):
        """Parse a single form starting at position."""
        # Implementation: balance angle brackets, extract keywords
        # This is simplified - real implementation needs proper parsing
        depth = 0
        i = start
        while i < len(content):
            if content[i] == '<':
                depth += 1
            elif content[i] == '>':
                depth -= 1
                if depth == 0:
                    form_text = content[start+1:i]
                    return self._parse_form_text(form_text), i+1
            i += 1
        return None, start

    def _parse_form_text(self, text):
        """Parse the interior of a form."""
        tokens = text.split()
        if not tokens:
            return None

        form_type = tokens[0]

        if form_type == 'OBJECT':
            return self._parse_object(tokens)
        elif form_type == 'ROUTINE':
            return self._parse_routine(tokens)
        # ... etc

    def _parse_object(self, tokens):
        """Parse OBJECT definition."""
        # Extract: name, properties, flags, etc.
        obj = {
            'type': 'OBJECT',
            'name': tokens[1] if len(tokens) > 1 else None,
            'properties': {}
        }

        # Parse properties (simplified)
        i = 2
        while i < len(tokens):
            if tokens[i].startswith('('):
                prop_name = tokens[i][1:]
                prop_value = []
                i += 1
                while i < len(tokens) and not tokens[i].endswith(')'):
                    prop_value.append(tokens[i])
                    i += 1
                if i < len(tokens):
                    prop_value.append(tokens[i][:-1])
                obj['properties'][prop_name] = prop_value
            i += 1

        return obj
```

**Tool 2: Code Generator**
```python
# zil_to_python.py - Generate Python from parsed ZIL

class PythonGenerator:
    """Generate Python code from ZIL AST."""

    def generate_object_class(self, obj_def):
        """Generate Python class for a ZIL object."""
        name = self._pythonize_name(obj_def['name'])
        props = obj_def['properties']

        # Determine class type
        base_class = self._determine_base_class(props)

        code = f"class {name}({base_class}):\n"
        code += f"    \"\"\"Auto-generated from ZIL.\"\"\"\n"
        code += f"    def __init__(self):\n"
        code += f"        super().__init__(\n"
        code += f"            id='{obj_def['name']}',\n"

        # Add properties
        if 'DESC' in props:
            code += f"            short_desc='{props['DESC'][0]}',\n"

        if 'SYNONYM' in props:
            code += f"            synonyms={props['SYNONYM']},\n"

        if 'FLAGS' in props:
            flags = ' | '.join(f'ObjectFlag.{f}' for f in props['FLAGS'])
            code += f"            flags={flags},\n"

        code += "        )\n"

        return code

    def _determine_base_class(self, props):
        """Determine which base class to use."""
        if 'CONTBIT' in props.get('FLAGS', []):
            return 'Container'
        elif 'ACTORBIT' in props.get('FLAGS', []):
            return 'Actor'
        # Check if it's a room (has exits)
        elif any(k in ['NORTH', 'SOUTH', 'EAST', 'WEST'] for k in props):
            return 'Room'
        else:
            return 'Item'
```

---

## PART 8: TESTING STRATEGY

### 8.1 Unit Tests

```python
# tests/test_parser.py

def test_simple_verb():
    """Test parsing simple one-word verbs."""
    parser = Parser(GRAMMAR, world)

    cmd = parser.parse_text("inventory")
    assert cmd.verb == Verb.INVENTORY
    assert cmd.direct_object is None

def test_verb_object():
    """Test parsing VERB OBJECT."""
    world.current_room = rooms.west_of_house
    world.current_room.contents.append(items.mailbox)

    cmd = parser.parse_text("open mailbox")
    assert cmd.verb == Verb.OPEN
    assert cmd.direct_object == items.mailbox

def test_verb_object_preposition_object():
    """Test parsing VERB OBJECT PREP OBJECT."""
    world.player.inventory.append(items.sword)
    world.current_room.contents.append(npcs.troll)

    cmd = parser.parse_text("attack troll with sword")
    assert cmd.verb == Verb.ATTACK
    assert cmd.direct_object == npcs.troll
    assert cmd.indirect_object == items.sword

def test_adjective_disambiguation():
    """Test adjectives for disambiguation."""
    world.current_room.contents.extend([
        items.brass_lantern,
        items.lamp,
    ])

    cmd = parser.parse_text("take brass lamp")
    assert cmd.direct_object == items.brass_lantern
```

### 8.2 Integration Tests

```python
# tests/test_game_logic.py

def test_take_drop_cycle():
    """Test taking and dropping an object."""
    game = GameEngine()
    game.start()

    # Start at West of House
    assert game.state.current_room.id == 'WEST-OF-HOUSE'

    # Go around to mailbox
    game.execute_text("open mailbox")
    assert items.mailbox.is_open

    game.execute_text("take leaflet")
    assert items.leaflet in game.state.player.inventory

    game.execute_text("read leaflet")
    # Check output contains expected text

def test_darkness_and_light():
    """Test lighting model."""
    game = GameEngine()

    # Enter cellar without light
    game.execute_text("open window")
    game.execute_text("enter")
    game.execute_text("down")

    # Should be dark
    assert not game.state.is_lit()

    # Try to move in darkness -> eaten by grue
    game.execute_text("north")
    assert game.state.player.is_dead
```

### 8.3 Regression Tests

Create a transcript of the original Zork I game, then replay it in Python version:

```python
# tests/test_regression.py

def test_walkthrough():
    """Test full game walkthrough matches original."""
    with open('tests/walkthrough.txt') as f:
        commands = f.readlines()

    game = GameEngine()
    game.start()

    for command in commands:
        output = game.execute_text(command.strip())
        # Compare output to expected (could use snapshot testing)
```

---

## PART 9: ADVANCED FEATURES & OPTIMIZATIONS

### 9.1 Optional: Modern Enhancements

While maintaining fidelity to the original, consider:

1. **Better Error Messages**
   - Original: "You can't see any foo here!"
   - Enhanced: "You can't see any foo here! (Did you mean: foobar?)"

2. **Undo/Redo**
   - Save state after each move
   - Allow player to undo mistaken commands

3. **Better Save Format**
   - JSON instead of binary for portability
   - Multiple save slots
   - Auto-save

4. **Accessibility**
   - Screen reader support
   - Configurable text size/colors
   - Text-to-speech output

5. **Modern UI Options**
   - Web interface (Flask/FastAPI)
   - GUI with Tkinter/PyQt
   - Keep CLI as default

### 9.2 Performance Considerations

The original game runs on a Z-Machine with severe constraints. Python version will be much faster, but:

- **Object Lookup**: Use dictionaries for O(1) lookup
  ```python
  # Instead of linear search
  def find_object(id):
      for obj in all_objects:
          if obj.id == id:
              return obj

  # Use dict
  objects_by_id = {obj.id: obj for obj in all_objects}
  def find_object(id):
      return objects_by_id.get(id)
  ```

- **Visibility Checks**: Cache results during each turn
  ```python
  class GameState:
      def __init__(self):
          self._visible_cache = None

      def get_visible_objects(self):
          if self._visible_cache is None:
              self._visible_cache = self._compute_visible()
          return self._visible_cache

      def invalidate_visibility(self):
          self._visible_cache = None
  ```

- **Parser Optimization**: Pre-compile regexes, use tries for vocabulary

---

## PART 10: DELIVERABLES & DOCUMENTATION

### 10.1 Final Project Structure

```
zork1_python/
├── README.md                   # User documentation
├── CONVERSION.md               # Conversion notes and decisions
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── main.py                     # Entry point
├── core/
│   ├── engine.py              # Game loop
│   ├── state.py               # Game state
│   ├── clock.py               # Timing system
│   └── constants.py           # Constants
├── parser/
│   ├── lexer.py               # Tokenization
│   ├── parser.py              # Command parsing
│   ├── grammar.py             # Grammar rules
│   └── vocabulary.py          # Word lists
├── objects/
│   ├── base.py                # GameObject base
│   ├── room.py                # Room class
│   ├── item.py                # Item class
│   ├── actor.py               # Actor/NPC class
│   └── container.py           # Container class
├── world_data/
│   ├── rooms.py               # Room definitions
│   ├── items.py               # Item definitions
│   └── npcs.py                # NPC definitions
├── actions/
│   ├── verbs.py               # Verb handlers
│   └── item_actions.py        # Item-specific actions
├── utils/
│   ├── output.py              # Output formatting
│   ├── flags.py               # Flag definitions
│   └── helpers.py             # Utilities
├── tests/
│   ├── test_parser.py
│   ├── test_objects.py
│   ├── test_game_logic.py
│   └── test_regression.py
└── docs/
    ├── architecture.md        # System architecture
    ├── zil_reference.md       # ZIL language reference
    └── api.md                 # Python API docs
```

### 10.2 Documentation Requirements

**README.md** should include:
- Installation instructions
- How to run the game
- Basic gameplay commands
- Credits (original Infocom authors + conversion credits)

**CONVERSION.md** should document:
- Major design decisions
- Differences from original
- Known issues/limitations
- Areas of uncertainty

**Code Comments** should explain:
- Complex algorithms (especially parser)
- ZIL → Python mapping for non-obvious conversions
- Game logic that isn't self-explanatory

---

## PART 11: RISK ASSESSMENT & MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Parser too complex to port | High | Critical | Start with subset, iterate |
| Game logic bugs hard to find | High | High | Extensive testing, regression tests |
| Performance issues | Low | Medium | Profile and optimize hotspots |
| Incomplete ZIL understanding | Medium | High | Reference ZILF compiler, ask community |
| Scope creep | Medium | Medium | Strict adherence to original, no new features initially |

---

## PART 12: ALTERNATIVE APPROACHES

### Approach A: Interpreter (Not Recommended)
Build a ZIL interpreter in Python that runs the original .zil files.

**Pros:**
- 100% faithful to original
- No conversion errors

**Cons:**
- Extremely complex
- Requires implementing ZIL runtime
- Harder to maintain/extend

### Approach B: Transpiler (Recommended)
Build a ZIL→Python transpiler that generates Python source.

**Pros:**
- Automated conversion of data
- Can manually fix generated code
- Best of both worlds

**Cons:**
- Still need to write transpiler
- Generated code may be messy

### Approach C: Manual Port (Most Practical)
Hand-convert ZIL to Python with helper scripts for data extraction.

**Pros:**
- Full control over code quality
- Easier to understand/maintain
- Can modernize where appropriate

**Cons:**
- Time-consuming
- Risk of translation errors

**RECOMMENDED: Hybrid of B + C**
- Auto-generate object definitions
- Manually port game logic
- Write comprehensive tests

---

## PART 13: REFERENCE RESOURCES

1. **ZIL Documentation:**
   - ZILF Documentation: http://zilf.io
   - ZIL Language Reference: https://www.inform-fiction.org/zmachine/standards/
   - Infocom Source Code (this repo)

2. **Python Libraries:**
   - `dataclasses` - For object definitions
   - `enum` - For flags and constants
   - `typing` - For type hints
   - `pytest` - For testing
   - `click` - For CLI interface
   - `colorama` - For colored output (optional)

3. **Similar Projects:**
   - Inform 7 - Modern IF system
   - TADS 3 - Text adventure system
   - Twine - Choice-based IF

---

## SUMMARY: CONVERSION ROADMAP

### TL;DR - Quick Start

1. **Week 1:** Set up project structure, create base classes
2. **Week 2:** Extract and convert all object/room definitions
3. **Week 3:** Build game engine and clock system
4. **Week 4-6:** Build parser (hardest part!)
5. **Week 6-7:** Implement verbs and actions
6. **Week 7-8:** Convert game-specific logic
7. **Week 8-10:** Test, debug, polish

### Key Success Factors

✅ **Start Small:** Get "look", "inventory", "quit" working first
✅ **Test Early:** Write tests from day one
✅ **Reference Original:** Play original game frequently to compare behavior
✅ **Document Decisions:** Keep notes on conversion choices
✅ **Iterate:** Don't try to be perfect on first pass

### Estimated Effort

- **If you know Python well:** 100-150 hours (2-3 months part-time)
- **Learning Python too:** 200-300 hours (4-6 months part-time)
- **With team of 2-3:** 60-80 hours each (1-2 months)

### Critical Path Items

The parser is the bottleneck. Everything else can proceed in parallel, but the parser (gparser.zil, ~3000 lines) is:
- The most complex component
- The least object-oriented (heavy procedural code)
- The most ZIL-idiomatic (uses many macros, advanced features)

**Recommendation:** Tackle parser in stages:
1. Simple commands (inventory, quit, look)
2. Single object (take lamp, drop sword)
3. Two objects (put lamp in case)
4. Multiple objects (take all, drop all except lamp)
5. Ambiguity resolution (which one?)
6. Pronouns (take it, examine them)

---

## FINAL THOUGHTS

Converting Zork I from ZIL to Python is a **substantial but achievable** project. The main challenges are:

1. **Understanding ZIL** - It's a Lisp dialect from the 1980s with limited documentation
2. **Parser Complexity** - Natural language parsing is inherently complex
3. **Maintaining Fidelity** - Need to match original behavior exactly

However, the benefits are significant:
- **Educational** - Learn about language design, parsers, game engines
- **Historical Preservation** - Make classic game more accessible
- **Extensibility** - Python code easier to modify than ZIL

**Success depends on:**
- Methodical approach (don't try to do everything at once)
- Comprehensive testing (regression tests against original)
- Community support (reference ZILF, ask questions)
- Patience (this is months of work, not weeks)

**Good luck! May you not be eaten by a grue.** 🕯️

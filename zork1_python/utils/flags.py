"""
Object flags for Zork I game objects.

This module defines all the flag bits used by game objects, converted from
the ZIL FLAGS system to Python IntFlag enums.
"""

from enum import IntFlag, auto


class ObjectFlag(IntFlag):
    """
    Flags for game object properties.

    These flags are used to mark various properties and capabilities of
    game objects. Multiple flags can be combined using bitwise OR.

    Converted from ZIL FLAGS definitions in gglobals.zil and 1dungeon.zil.
    """

    # Core object properties
    INVISIBLE = auto()      # Object is invisible to player
    NDESCBIT = auto()       # No description (don't list in room descriptions)
    TOUCHBIT = auto()       # Can be touched/manipulated

    # Container/Surface properties
    CONTBIT = auto()        # Is a container
    SURFACEBIT = auto()     # Is a surface (can put things on it)
    OPENBIT = auto()        # Container/door is open
    TRANSBIT = auto()       # Transparent (can see contents when closed)
    SEARCHBIT = auto()      # Can be searched

    # Object interaction
    TAKEBIT = auto()        # Can be taken/picked up
    TRYTAKEBIT = auto()     # Player can try to take (but may fail)
    DOORBIT = auto()        # Is a door
    CLIMBBIT = auto()       # Can be climbed

    # Light and visibility
    LIGHTBIT = auto()       # Provides light
    ONBIT = auto()          # Light source is turned on
    FLAMEBIT = auto()       # Is a flame (can burn things)

    # Character/Actor properties
    ACTORBIT = auto()       # Is an actor/NPC
    PERSONBIT = auto()      # Is a person
    FEMALEBIT = auto()      # Is female (for pronoun handling)

    # Combat and interaction
    WEAPONBIT = auto()      # Is a weapon
    FIGHTBIT = auto()       # Can be fought
    STAGGERED = auto()      # Is staggered (combat state)

    # Item properties
    WEARBIT = auto()        # Can be worn
    FOODBIT = auto()        # Is edible
    DRINKBIT = auto()       # Is drinkable
    READBIT = auto()        # Can be read
    BURNBIT = auto()        # Can be burned
    TOOLBIT = auto()        # Is a tool

    # Special properties
    RMUNGBIT = auto()       # Room mung bit (special room state)
    RLANDBIT = auto()       # Room land bit
    SACREDBIT = auto()      # Is sacred/magical
    VEHBIT = auto()         # Is a vehicle
    INTEGBIT = auto()       # Integral (can't be separated)
    VOWELBIT = auto()       # Name starts with vowel (for "a" vs "an")

    # Game mechanics
    MOVEABLE = auto()       # Can be moved by player
    LOCKEDBIT = auto()      # Is locked
    OPENABLE = auto()       # Can be opened


class RoomFlag(IntFlag):
    """
    Flags specific to rooms.

    These control room behavior and properties.
    """

    RLANDBIT = auto()       # Land room (vs water, etc.)
    RMUNGBIT = auto()       # Room mung bit (special state)
    SACREDBIT = auto()      # Sacred room (special rules)
    MAZEROOM = auto()       # Is part of a maze
    OUTSIDEBIT = auto()     # Is outside



class VerbFlag(IntFlag):
    """
    Flags for verb behavior.
    """

    DARKBIT = auto()        # Can be used in darkness
    STAGGERBIT = auto()     # Affected by staggered state


def has_flag(obj, flag: ObjectFlag) -> bool:
    """
    Check if an object has a specific flag.

    Args:
        obj: Object with a 'flags' attribute
        flag: Flag to check for

    Returns:
        True if object has the flag, False otherwise
    """
    if not hasattr(obj, 'flags'):
        return False
    return bool(obj.flags & flag)


def set_flag(obj, flag: ObjectFlag) -> None:
    """
    Set a flag on an object.

    Args:
        obj: Object with a 'flags' attribute
        flag: Flag to set
    """
    if hasattr(obj, 'flags'):
        obj.flags |= flag


def clear_flag(obj, flag: ObjectFlag) -> None:
    """
    Clear a flag on an object.

    Args:
        obj: Object with a 'flags' attribute
        flag: Flag to clear
    """
    if hasattr(obj, 'flags'):
        obj.flags &= ~flag


def toggle_flag(obj, flag: ObjectFlag) -> None:
    """
    Toggle a flag on an object.

    Args:
        obj: Object with a 'flags' attribute
        flag: Flag to toggle
    """
    if hasattr(obj, 'flags'):
        obj.flags ^= flag

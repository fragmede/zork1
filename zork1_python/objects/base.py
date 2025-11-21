"""
Base GameObject class for Zork I.

This module defines the base GameObject class that all game entities
(rooms, items, actors, etc.) inherit from. It implements the core
functionality of ZIL OBJECTs.
"""

from typing import Optional, Set, List, Callable, Any, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from ..utils.flags import ObjectFlag


class ActionResult(Enum):
    """Results from action handlers."""
    NOT_HANDLED = 0      # Action not handled, try next handler
    HANDLED = 1          # Action handled successfully
    BLOCKED = 2          # Action blocked/failed


class GameObject:
    """
    Base class for all game objects.

    This is the Python equivalent of ZIL <OBJECT ...> definitions.
    All rooms, items, actors, and other game entities inherit from this.

    Attributes:
        id: Unique identifier for this object (ZIL object name)
        synonyms: List of words that refer to this object
        adjectives: List of adjectives that can describe this object
        short_desc: Short description (one line)
        long_desc: Long description (multiple lines, first time seen)
        flags: Bit flags for object properties
        location: Current location/container of this object
        contents: List of objects contained in this object
        properties: Dictionary of additional properties
        action_handler: Optional function to handle actions on this object
    """

    def __init__(
        self,
        id: str,
        synonyms: Optional[List[str]] = None,
        adjectives: Optional[List[str]] = None,
        short_desc: str = "",
        long_desc: str = "",
        flags: int = 0,
        location: Optional['GameObject'] = None,
        properties: Optional[dict] = None,
        action_handler: Optional[Callable] = None
    ):
        """
        Initialize a game object.

        Args:
            id: Unique identifier (uppercase, like ZIL names)
            synonyms: Words that refer to this object
            adjectives: Adjectives that describe this object
            short_desc: Brief description
            long_desc: Detailed description
            flags: ObjectFlag bits
            location: Initial location (parent object)
            properties: Additional properties as dict
            action_handler: Function to handle actions (PRSA, PRSO, PRSI)
        """
        self.id = id
        self.synonyms = synonyms or []
        self.adjectives = adjectives or []
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.flags = flags
        self._location: Optional[GameObject] = None
        self.contents: List[GameObject] = []
        self.properties = properties or {}
        self.action_handler = action_handler

        # First-time seen flag
        self.seen = False

        # Move to initial location if specified
        if location is not None:
            self.move_to(location)

    @property
    def location(self) -> Optional['GameObject']:
        """Get current location of this object."""
        return self._location

    def move_to(self, new_location: Optional['GameObject']) -> None:
        """
        Move this object to a new location.

        This handles the containment hierarchy, removing from old location
        and adding to new location.

        Args:
            new_location: New container/room for this object, or None
        """
        # Remove from old location
        if self._location is not None:
            if self in self._location.contents:
                self._location.contents.remove(self)

        # Add to new location
        self._location = new_location
        if new_location is not None:
            if self not in new_location.contents:
                new_location.contents.append(self)

    def is_in(self, container: 'GameObject') -> bool:
        """
        Check if this object is directly in a container.

        Args:
            container: Container to check

        Returns:
            True if this object's location is the container
        """
        return self._location == container

    def is_accessible_to(self, actor: 'GameObject') -> bool:
        """
        Check if this object is accessible to an actor.

        An object is accessible if it's:
        1. In the same room as the actor
        2. In the actor's inventory
        3. In an open/transparent container in the room or inventory

        Args:
            actor: The actor trying to access this object

        Returns:
            True if accessible, False otherwise
        """
        from ..utils.flags import ObjectFlag

        # In actor's inventory
        if self.is_in(actor):
            return True

        # In same room
        actor_room = actor.get_room()
        if actor_room and self.is_in(actor_room):
            return True

        # In a container in the room or inventory
        container = self._location
        while container is not None:
            # Check if we've reached the actor's room or inventory
            if container == actor or container == actor_room:
                # Check all containers in the chain are open/transparent
                return self._containers_accessible()

            container = container._location

        return False

    def _containers_accessible(self) -> bool:
        """
        Check if all containers between this object and the room/actor are accessible.

        Returns:
            True if all containers are open or transparent
        """
        from ..utils.flags import ObjectFlag

        container = self._location
        while container is not None:
            # If container is not open and not transparent, can't access
            if hasattr(container, 'flags'):
                if not (container.flags & ObjectFlag.OPENBIT or
                        container.flags & ObjectFlag.TRANSBIT):
                    return False
            container = container._location

        return True

    def get_room(self) -> Optional['GameObject']:
        """
        Get the room this object is in.

        Traverses up the containment hierarchy until finding a room.

        Returns:
            The room object, or None if not in a room
        """
        from .room import Room

        obj = self
        while obj is not None:
            if isinstance(obj, Room):
                return obj
            obj = obj._location
        return None

    def has_flag(self, flag: 'ObjectFlag') -> bool:
        """
        Check if this object has a specific flag.

        Args:
            flag: Flag to check

        Returns:
            True if flag is set
        """
        return bool(self.flags & flag)

    def set_flag(self, flag: 'ObjectFlag') -> None:
        """
        Set a flag on this object.

        Args:
            flag: Flag to set
        """
        self.flags |= flag

    def clear_flag(self, flag: 'ObjectFlag') -> None:
        """
        Clear a flag on this object.

        Args:
            flag: Flag to clear
        """
        self.flags &= ~flag

    def action(self, verb: Any, direct_obj: 'GameObject', indirect_obj: Optional['GameObject'] = None) -> ActionResult:
        """
        Handle an action performed on this object.

        This is called when the player performs an action on this object.
        Subclasses can override this or provide an action_handler function.

        Args:
            verb: The verb being performed
            direct_obj: Direct object of the action (usually self)
            indirect_obj: Indirect object, if any

        Returns:
            ActionResult indicating how the action was handled
        """
        if self.action_handler:
            result = self.action_handler(verb, direct_obj, indirect_obj)
            if result:
                return ActionResult.HANDLED
        return ActionResult.NOT_HANDLED

    def get_property(self, name: str, default: Any = None) -> Any:
        """
        Get a custom property value.

        Args:
            name: Property name
            default: Default value if property not found

        Returns:
            Property value or default
        """
        return self.properties.get(name, default)

    def set_property(self, name: str, value: Any) -> None:
        """
        Set a custom property value.

        Args:
            name: Property name
            value: Property value
        """
        self.properties[name] = value

    def matches(self, noun: Optional[str] = None, adjective: Optional[str] = None) -> bool:
        """
        Check if this object matches a noun and/or adjective.

        Used by the parser to find objects matching player input.

        Args:
            noun: Noun to match (checked against synonyms)
            adjective: Adjective to match

        Returns:
            True if object matches the criteria
        """
        # Check noun
        if noun is not None:
            if noun not in self.synonyms:
                return False

        # Check adjective
        if adjective is not None:
            if adjective not in self.adjectives:
                return False

        return True

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<{self.__class__.__name__} {self.id}>"

    def __str__(self) -> str:
        """String representation for display."""
        return self.short_desc or self.id

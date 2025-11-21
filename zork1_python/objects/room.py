"""
Room class for Zork I.

Rooms are the locations where gameplay takes place. This module defines
the Room class which represents a location in the game world.
"""

from typing import Optional, Dict, Callable, Any
from .base import GameObject, ActionResult
from ..utils.flags import RoomFlag


class Room(GameObject):
    """
    A room/location in the game world.

    Rooms are special GameObject instances that represent locations.
    They can have exits to other rooms and contain items and actors.

    Attributes:
        exits: Dictionary mapping direction names to Room objects or functions
        visited: Whether player has been in this room before
        room_action: Optional function called when entering/in room
        light_level: Amount of light in room (0 = dark)
    """

    def __init__(
        self,
        id: str,
        short_desc: str = "",
        long_desc: str = "",
        flags: int = 0,
        exits: Optional[Dict[str, Any]] = None,
        room_action: Optional[Callable] = None,
        properties: Optional[dict] = None
    ):
        """
        Initialize a room.

        Args:
            id: Unique room identifier
            short_desc: Room name
            long_desc: Detailed room description
            flags: RoomFlag bits
            exits: Dictionary of direction -> Room/function mappings
            room_action: Function called for room-specific actions
            properties: Additional room properties
        """
        super().__init__(
            id=id,
            short_desc=short_desc,
            long_desc=long_desc,
            flags=flags,
            location=None,  # Rooms don't have locations
            properties=properties
        )

        self.exits: Dict[str, Any] = exits or {}
        self.visited = False
        self.room_action = room_action
        self.light_level = 1  # Default to lit

    def get_exit(self, direction: str) -> Optional['Room']:
        """
        Get the room in a given direction.

        Args:
            direction: Direction name (NORTH, SOUTH, EAST, WEST, etc.)

        Returns:
            The room object in that direction, or None if no exit
        """
        exit_data = self.exits.get(direction.upper())

        if exit_data is None:
            return None

        # If it's a function, call it to get the actual room
        if callable(exit_data):
            return exit_data()

        # Otherwise it's a room object or room ID
        return exit_data

    def add_exit(self, direction: str, target: Any) -> None:
        """
        Add an exit to this room.

        Args:
            direction: Direction name
            target: Target room or function that returns a room
        """
        self.exits[direction.upper()] = target

    def remove_exit(self, direction: str) -> None:
        """
        Remove an exit from this room.

        Args:
            direction: Direction name to remove
        """
        if direction.upper() in self.exits:
            del self.exits[direction.upper()]

    def is_lit(self) -> bool:
        """
        Check if this room is lit (player can see).

        A room is lit if:
        1. It has natural light (light_level > 0)
        2. It contains a light source that's on
        3. The player is carrying a light source that's on

        Returns:
            True if room is lit, False if dark
        """
        from ..utils.flags import ObjectFlag

        # Room has natural light
        if self.light_level > 0:
            return True

        # Check for light sources in room or player's inventory
        # This will be implemented when we have game state access
        # For now, just check the room contents
        for obj in self.contents:
            if obj.has_flag(ObjectFlag.LIGHTBIT) and obj.has_flag(ObjectFlag.ONBIT):
                return True

        return False

    def describe(self, verbose: bool = False) -> str:
        """
        Get a description of this room.

        Args:
            verbose: If True, always show long description

        Returns:
            Room description string
        """
        parts = []

        # Room name
        parts.append(self.short_desc)
        parts.append("")

        # Description
        if verbose or not self.visited:
            parts.append(self.long_desc)
        else:
            # Brief mode - just show room name and exits
            pass

        # List visible objects
        visible_objects = [obj for obj in self.contents
                          if not obj.has_flag(getattr(obj, 'flags', 0) &
                                            (1 << 0))]  # Not NDESCBIT

        if visible_objects:
            parts.append("")
            for obj in visible_objects:
                # Use FDESC if available and not seen, else LDESC
                if hasattr(obj, 'fdesc') and not obj.seen:
                    parts.append(obj.fdesc)
                    obj.seen = True
                elif hasattr(obj, 'ldesc'):
                    parts.append(obj.ldesc)
                else:
                    parts.append(f"There is {obj.short_desc} here.")

        return "\n".join(parts)

    def on_enter(self, actor: GameObject) -> ActionResult:
        """
        Called when an actor enters this room.

        Args:
            actor: The actor entering the room

        Returns:
            ActionResult indicating if anything special happened
        """
        if self.room_action:
            # Room-specific action handler
            result = self.room_action('ENTER', actor, None)
            if result:
                return ActionResult.HANDLED

        # Mark as visited
        self.visited = True

        return ActionResult.NOT_HANDLED

    def on_look(self) -> ActionResult:
        """
        Called when player looks around the room.

        Returns:
            ActionResult
        """
        if self.room_action:
            result = self.room_action('LOOK', None, None)
            if result:
                return ActionResult.HANDLED

        return ActionResult.NOT_HANDLED

    def get_visible_objects(self) -> list:
        """
        Get all visible objects in this room.

        Returns:
            List of visible GameObject instances
        """
        from ..utils.flags import ObjectFlag

        visible = []
        for obj in self.contents:
            if not obj.has_flag(ObjectFlag.INVISIBLE):
                visible.append(obj)

        return visible

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Room {self.id}: {self.short_desc}>"

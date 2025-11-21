"""
Container class for Zork I.

Containers are objects that can hold other objects (bags, boxes, etc.).
This module defines the Container class.
"""

from typing import Optional, Callable, List
from .item import Item
from .base import GameObject
from ..utils.flags import ObjectFlag


class Container(Item):
    """
    A container that can hold other objects.

    Containers are items that can contain other items. They can be
    open or closed, locked or unlocked.

    Attributes:
        capacity: Maximum weight this container can hold
        is_surface: Whether this is a surface (vs an internal container)
    """

    def __init__(
        self,
        id: str,
        synonyms: Optional[List[str]] = None,
        adjectives: Optional[List[str]] = None,
        short_desc: str = "",
        long_desc: str = "",
        fdesc: str = "",
        ldesc: str = "",
        flags: int = 0,
        location: Optional[GameObject] = None,
        size: int = 5,
        capacity: int = 100,
        is_surface: bool = False,
        action_handler: Optional[Callable] = None,
        properties: Optional[dict] = None
    ):
        """
        Initialize a container.

        Args:
            id: Unique identifier
            synonyms: Words that refer to this container
            adjectives: Adjectives describing this container
            short_desc: Brief description
            long_desc: Detailed description
            fdesc: First-time description
            ldesc: Later description
            flags: ObjectFlag bits (should include CONTBIT)
            location: Initial location
            size: Size of the container itself
            capacity: Maximum weight of contents
            is_surface: True if surface (table, etc.), False if container
            action_handler: Custom action handler
            properties: Additional properties
        """
        # Ensure container flag is set
        flags |= ObjectFlag.CONTBIT
        if is_surface:
            flags |= ObjectFlag.SURFACEBIT

        super().__init__(
            id=id,
            synonyms=synonyms,
            adjectives=adjectives,
            short_desc=short_desc,
            long_desc=long_desc,
            fdesc=fdesc,
            ldesc=ldesc,
            flags=flags,
            location=location,
            size=size,
            action_handler=action_handler,
            properties=properties
        )

        self.capacity = capacity
        self.is_surface = is_surface

    @property
    def is_open(self) -> bool:
        """Check if this container is open."""
        # Surfaces are always "open"
        if self.is_surface:
            return True
        return self.has_flag(ObjectFlag.OPENBIT)

    @property
    def is_openable(self) -> bool:
        """Check if this container can be opened."""
        # Surfaces can't be opened/closed
        if self.is_surface:
            return False
        return self.has_flag(ObjectFlag.OPENABLE)

    @property
    def is_transparent(self) -> bool:
        """Check if you can see contents when closed."""
        return self.has_flag(ObjectFlag.TRANSBIT)

    @property
    def is_locked(self) -> bool:
        """Check if this container is locked."""
        return self.has_flag(ObjectFlag.LOCKEDBIT)

    def open(self) -> tuple[bool, str]:
        """
        Open this container.

        Returns:
            Tuple of (success, message)
        """
        if self.is_surface:
            return False, "You can't open that."

        if not self.is_openable:
            return False, "You can't open that."

        if self.is_locked:
            return False, f"The {self.short_desc} is locked."

        if self.is_open:
            return False, f"The {self.short_desc} is already open."

        self.set_flag(ObjectFlag.OPENBIT)
        return True, f"Opened."

    def close(self) -> tuple[bool, str]:
        """
        Close this container.

        Returns:
            Tuple of (success, message)
        """
        if self.is_surface:
            return False, "You can't close that."

        if not self.is_openable:
            return False, "You can't close that."

        if not self.is_open:
            return False, f"The {self.short_desc} is already closed."

        self.clear_flag(ObjectFlag.OPENBIT)
        return True, f"Closed."

    def lock(self) -> tuple[bool, str]:
        """
        Lock this container.

        Returns:
            Tuple of (success, message)
        """
        if self.is_surface:
            return False, "You can't lock that."

        if not self.is_open:
            # Must be closed to lock
            if self.is_locked:
                return False, f"The {self.short_desc} is already locked."

            self.set_flag(ObjectFlag.LOCKEDBIT)
            return True, "Locked."
        else:
            return False, f"The {self.short_desc} must be closed first."

    def unlock(self) -> tuple[bool, str]:
        """
        Unlock this container.

        Returns:
            Tuple of (success, message)
        """
        if self.is_surface:
            return False, "You can't unlock that."

        if not self.is_locked:
            return False, f"The {self.short_desc} isn't locked."

        self.clear_flag(ObjectFlag.LOCKEDBIT)
        return True, "Unlocked."

    def can_hold(self, obj: GameObject) -> bool:
        """
        Check if this container can hold an object.

        Args:
            obj: Object to check

        Returns:
            True if there's room for the object
        """
        # Calculate current weight
        current_weight = sum(
            o.get_weight() if hasattr(o, 'get_weight') else getattr(o, 'size', 5)
            for o in self.contents
        )

        # Get object weight
        obj_weight = obj.get_weight() if hasattr(obj, 'get_weight') else getattr(obj, 'size', 5)

        return (current_weight + obj_weight) <= self.capacity

    def get_visible_contents(self) -> List[GameObject]:
        """
        Get visible contents of this container.

        Contents are visible if:
        - Container is open, OR
        - Container is transparent

        Returns:
            List of visible objects
        """
        if self.is_open or self.is_transparent or self.is_surface:
            return [obj for obj in self.contents
                   if not obj.has_flag(ObjectFlag.INVISIBLE)]
        return []

    def __repr__(self) -> str:
        """String representation for debugging."""
        state = "SURFACE" if self.is_surface else ("OPEN" if self.is_open else "CLOSED")
        count = len(self.contents)
        return f"<Container {self.id}: {self.short_desc} [{state}, {count} items]>"

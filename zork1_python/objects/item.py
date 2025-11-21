"""
Item class for Zork I.

Items are objects that can typically be picked up and manipulated by the player.
This module defines the Item class for game items.
"""

from typing import Optional, Callable, List
from .base import GameObject, ActionResult
from ..utils.flags import ObjectFlag


class Item(GameObject):
    """
    An item in the game world.

    Items are objects that can typically be taken, dropped, examined, etc.
    They inherit all GameObject functionality and add item-specific properties.

    Attributes:
        size: Size/weight of the item (for inventory limits)
        value: Point value of the item
        treasure_value: Point value if deposited in trophy case
        fdesc: First-time description (when first seen)
        ldesc: Long description (subsequent times)
        text: Text on readable items
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
        value: int = 0,
        treasure_value: int = 0,
        text: str = "",
        action_handler: Optional[Callable] = None,
        properties: Optional[dict] = None
    ):
        """
        Initialize an item.

        Args:
            id: Unique identifier
            synonyms: Words that refer to this item
            adjectives: Adjectives describing this item
            short_desc: Brief description
            long_desc: Detailed description
            fdesc: First-time description (seen in room)
            ldesc: Later description (seen in room)
            flags: ObjectFlag bits
            location: Initial location
            size: Size/weight (for carrying capacity)
            value: Point value
            treasure_value: Treasure point value
            text: Text on readable items
            action_handler: Custom action handler
            properties: Additional properties
        """
        super().__init__(
            id=id,
            synonyms=synonyms,
            adjectives=adjectives,
            short_desc=short_desc,
            long_desc=long_desc,
            flags=flags,
            location=location,
            action_handler=action_handler,
            properties=properties
        )

        self.size = size
        self.value = value
        self.treasure_value = treasure_value
        self.fdesc = fdesc
        self.ldesc = ldesc
        self.text = text

    @property
    def is_takeable(self) -> bool:
        """Check if this item can be taken."""
        return self.has_flag(ObjectFlag.TAKEBIT)

    @property
    def is_treasure(self) -> bool:
        """Check if this item is a treasure."""
        return self.treasure_value > 0

    @property
    def is_weapon(self) -> bool:
        """Check if this item is a weapon."""
        return self.has_flag(ObjectFlag.WEAPONBIT)

    @property
    def is_readable(self) -> bool:
        """Check if this item can be read."""
        return self.has_flag(ObjectFlag.READBIT) or bool(self.text)

    @property
    def is_light_source(self) -> bool:
        """Check if this item provides light."""
        return self.has_flag(ObjectFlag.LIGHTBIT)

    @property
    def is_on(self) -> bool:
        """Check if this light source is turned on."""
        return self.has_flag(ObjectFlag.ONBIT)

    def turn_on(self) -> bool:
        """
        Turn on this light source.

        Returns:
            True if successful, False if not a light source
        """
        if not self.is_light_source:
            return False

        self.set_flag(ObjectFlag.ONBIT)
        return True

    def turn_off(self) -> bool:
        """
        Turn off this light source.

        Returns:
            True if successful, False if not a light source
        """
        if not self.is_light_source:
            return False

        self.clear_flag(ObjectFlag.ONBIT)
        return True

    def read_text(self) -> Optional[str]:
        """
        Get the text on this item (if readable).

        Returns:
            The text, or None if not readable
        """
        if not self.is_readable:
            return None
        return self.text

    def get_weight(self) -> int:
        """
        Get the total weight of this item and its contents.

        Returns:
            Total size/weight
        """
        total = self.size

        # Add weight of contents if this is a container
        for obj in self.contents:
            if hasattr(obj, 'get_weight'):
                total += obj.get_weight()
            elif hasattr(obj, 'size'):
                total += obj.size

        return total

    def __repr__(self) -> str:
        """String representation for debugging."""
        flags_str = []
        if self.is_takeable:
            flags_str.append("TAKE")
        if self.is_treasure:
            flags_str.append("TREAS")
        if self.is_light_source:
            flags_str.append("LIGHT")

        flags = f" [{','.join(flags_str)}]" if flags_str else ""
        return f"<Item {self.id}: {self.short_desc}{flags}>"

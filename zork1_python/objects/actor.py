"""
Actor class for Zork I.

Actors are NPCs (non-player characters) that can interact with the player
and the world. This module defines the Actor class.
"""

from typing import Optional, Callable, List
from .base import GameObject, ActionResult
from ..utils.flags import ObjectFlag


class Actor(GameObject):
    """
    An actor/NPC in the game world.

    Actors are characters that can move, fight, and interact with
    the player. They have their own inventory and can perform actions.

    Attributes:
        health: Current health points
        max_health: Maximum health points
        strength: Combat strength
        is_hostile: Whether this actor is hostile to player
        ai_handler: Function that controls this actor's behavior
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
        health: int = 10,
        strength: int = 1,
        is_hostile: bool = False,
        ai_handler: Optional[Callable] = None,
        action_handler: Optional[Callable] = None,
        properties: Optional[dict] = None
    ):
        """
        Initialize an actor.

        Args:
            id: Unique identifier
            synonyms: Words that refer to this actor
            adjectives: Adjectives describing this actor
            short_desc: Brief description
            long_desc: Detailed description
            fdesc: First-time description
            ldesc: Later description
            flags: ObjectFlag bits (should include ACTORBIT)
            location: Initial location
            health: Starting health
            strength: Combat strength
            is_hostile: Whether hostile to player
            ai_handler: Function that controls AI behavior
            action_handler: Custom action handler
            properties: Additional properties
        """
        # Ensure actor flag is set
        flags |= ObjectFlag.ACTORBIT

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

        self.health = health
        self.max_health = health
        self.strength = strength
        self.is_hostile = is_hostile
        self.ai_handler = ai_handler
        self.fdesc = fdesc
        self.ldesc = ldesc

        # Actor state
        self.is_staggered = False
        self.is_dead = False

    @property
    def inventory(self) -> List[GameObject]:
        """Get this actor's inventory (alias for contents)."""
        return self.contents

    @property
    def is_alive(self) -> bool:
        """Check if this actor is alive."""
        return not self.is_dead and self.health > 0

    def take_damage(self, amount: int) -> tuple[int, bool]:
        """
        Apply damage to this actor.

        Args:
            amount: Amount of damage to apply

        Returns:
            Tuple of (actual damage taken, whether actor died)
        """
        if self.is_dead:
            return 0, True

        # Apply damage
        actual_damage = min(amount, self.health)
        self.health -= actual_damage

        # Check if dead
        if self.health <= 0:
            self.is_dead = True
            self.health = 0
            return actual_damage, True

        return actual_damage, False

    def heal(self, amount: int) -> int:
        """
        Heal this actor.

        Args:
            amount: Amount to heal

        Returns:
            Actual amount healed
        """
        if self.is_dead:
            return 0

        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        return self.health - old_health

    def can_carry(self, obj: GameObject) -> bool:
        """
        Check if this actor can carry an object.

        Args:
            obj: Object to check

        Returns:
            True if actor can carry the object
        """
        # Simple implementation - could be enhanced with carry limits
        return True

    def give_item(self, item: GameObject) -> bool:
        """
        Give an item to this actor.

        Args:
            item: Item to give

        Returns:
            True if successful
        """
        if not self.can_carry(item):
            return False

        item.move_to(self)
        return True

    def drop_item(self, item: GameObject) -> bool:
        """
        Drop an item from inventory.

        Args:
            item: Item to drop

        Returns:
            True if successful
        """
        if item not in self.contents:
            return False

        # Drop in current room
        room = self.get_room()
        if room:
            item.move_to(room)
            return True

        return False

    def tick(self) -> ActionResult:
        """
        Called each turn to let the actor take action.

        This calls the AI handler if one is defined.

        Returns:
            ActionResult from the AI handler
        """
        if not self.is_alive:
            return ActionResult.NOT_HANDLED

        if self.ai_handler:
            result = self.ai_handler(self)
            if result:
                return ActionResult.HANDLED

        return ActionResult.NOT_HANDLED

    def attack(self, target: 'Actor', weapon: Optional[GameObject] = None) -> tuple[bool, int, str]:
        """
        Attack another actor.

        Args:
            target: Actor to attack
            weapon: Optional weapon to use

        Returns:
            Tuple of (hit, damage, message)
        """
        import random

        if not self.is_alive:
            return False, 0, "You are dead and cannot attack."

        if not target.is_alive:
            return False, 0, f"The {target.short_desc} is already dead."

        # Simple combat calculation
        base_damage = self.strength

        # Weapon bonus
        if weapon and weapon.has_flag(ObjectFlag.WEAPONBIT):
            base_damage += weapon.get_property('damage', 1)

        # Random factor
        damage = random.randint(base_damage // 2, base_damage * 2)

        # Apply damage
        actual_damage, died = target.take_damage(damage)

        if died:
            message = f"The {target.short_desc} is killed!"
        elif actual_damage > 0:
            message = f"The {target.short_desc} takes {actual_damage} damage."
        else:
            message = f"The attack misses!"

        return actual_damage > 0, actual_damage, message

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = "DEAD" if self.is_dead else f"HP:{self.health}/{self.max_health}"
        hostile = " HOSTILE" if self.is_hostile else ""
        return f"<Actor {self.id}: {self.short_desc} [{status}{hostile}]>"

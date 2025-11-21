#!/usr/bin/env python3
"""
Zork I - Python Edition

A Python conversion of the classic Infocom game Zork I.
Original game by Marc Blank, Dave Lebling, Bruce Daniels, and Tim Anderson.
Python conversion based on the ZIL source code.

Usage:
    python main.py
"""

from .utils.output import OutputManager, tell
from .utils.flags import ObjectFlag
from .objects.room import Room
from .objects.item import Item
from .objects.container import Container
from .objects.actor import Actor


def create_demo_world():
    """
    Create a simple demo world to test the system.

    This creates a few rooms and objects to verify everything works.
    """
    # Create some rooms
    west_of_house = Room(
        id="WEST-OF-HOUSE",
        short_desc="West of House",
        long_desc="You are standing in an open field west of a white house, "
                  "with a boarded front door.",
        exits={}
    )

    kitchen = Room(
        id="KITCHEN",
        short_desc="Kitchen",
        long_desc="You are in the kitchen of the white house. A table seems to "
                  "have been used recently for the preparation of food. A passage "
                  "leads to the west and a dark staircase can be seen leading upward.",
        exits={}
    )

    # Connect rooms
    west_of_house.add_exit("ENTER", kitchen)
    kitchen.add_exit("WEST", west_of_house)

    # Create some items
    mailbox = Container(
        id="MAILBOX",
        synonyms=["mailbox", "box"],
        adjectives=["small"],
        short_desc="small mailbox",
        long_desc="The small mailbox is closed.",
        flags=ObjectFlag.OPENABLE,
        location=west_of_house,
        capacity=10
    )

    leaflet = Item(
        id="LEAFLET",
        synonyms=["leaflet", "booklet", "mail"],
        adjectives=["small"],
        short_desc="leaflet",
        long_desc="A small leaflet.",
        flags=ObjectFlag.TAKEBIT | ObjectFlag.READBIT,
        location=mailbox,
        text="WELCOME TO ZORK!\n\n"
             "ZORK is a game of adventure, danger, and low cunning. In it you will "
             "explore some of the most amazing territory ever seen by mortals. No "
             "computer should be without one!",
        size=1
    )

    lantern = Item(
        id="LANTERN",
        synonyms=["lantern", "lamp", "light"],
        adjectives=["brass"],
        short_desc="brass lantern",
        long_desc="A shiny brass lantern.",
        flags=ObjectFlag.TAKEBIT | ObjectFlag.LIGHTBIT | ObjectFlag.ONBIT,
        location=kitchen,
        size=5
    )

    return {
        'rooms': {
            'west_of_house': west_of_house,
            'kitchen': kitchen,
        },
        'items': {
            'mailbox': mailbox,
            'leaflet': leaflet,
            'lantern': lantern,
        }
    }


def demo():
    """Run a simple demo of the system."""
    output = OutputManager()

    output.tell("=" * 60)
    output.tell("ZORK I - PYTHON EDITION - FOUNDATION DEMO")
    output.tell("=" * 60)
    output.tell()

    # Create world
    world = create_demo_world()

    # Test room
    output.tell("Testing Room System:")
    output.tell("-" * 60)
    west = world['rooms']['west_of_house']
    output.tell(west.describe(verbose=True))
    output.tell()

    # Test container
    output.tell("Testing Container System:")
    output.tell("-" * 60)
    mailbox = world['items']['mailbox']
    output.tell(f"Mailbox is open: {mailbox.is_open}")
    output.tell(f"Mailbox contents: {len(mailbox.contents)} items")

    success, msg = mailbox.open()
    output.tell(msg)
    output.tell(f"Mailbox is now open: {mailbox.is_open}")

    if mailbox.contents:
        output.tell(f"Inside the mailbox: {mailbox.contents[0].short_desc}")

    output.tell()

    # Test item
    output.tell("Testing Item System:")
    output.tell("-" * 60)
    leaflet = world['items']['leaflet']
    output.tell(f"Item: {leaflet.short_desc}")
    output.tell(f"Is takeable: {leaflet.is_takeable}")
    output.tell(f"Is readable: {leaflet.is_readable}")

    if leaflet.is_readable:
        output.tell("\nReading the leaflet:")
        output.tell(leaflet.read_text())

    output.tell()

    # Test light source
    output.tell("Testing Light Source:")
    output.tell("-" * 60)
    lantern = world['items']['lantern']
    output.tell(f"Lantern: {lantern.short_desc}")
    output.tell(f"Is light source: {lantern.is_light_source}")
    output.tell(f"Is on: {lantern.is_on}")

    lantern.turn_off()
    output.tell(f"After turning off: {lantern.is_on}")

    lantern.turn_on()
    output.tell(f"After turning on: {lantern.is_on}")

    output.tell()

    # Test object flags
    output.tell("Testing Flag System:")
    output.tell("-" * 60)
    output.tell(f"Leaflet flags: {leaflet.flags}")
    output.tell(f"Has TAKEBIT: {leaflet.has_flag(ObjectFlag.TAKEBIT)}")
    output.tell(f"Has READBIT: {leaflet.has_flag(ObjectFlag.READBIT)}")
    output.tell(f"Has WEAPONBIT: {leaflet.has_flag(ObjectFlag.WEAPONBIT)}")

    output.tell()

    # Test object movement
    output.tell("Testing Object Movement:")
    output.tell("-" * 60)
    kitchen = world['rooms']['kitchen']
    output.tell(f"Leaflet location: {leaflet.location}")
    output.tell(f"Kitchen contents before: {len(kitchen.contents)} items")

    leaflet.move_to(kitchen)
    output.tell(f"Leaflet location after move: {leaflet.location}")
    output.tell(f"Kitchen contents after: {len(kitchen.contents)} items")
    output.tell(f"Mailbox contents after: {len(mailbox.contents)} items")

    output.tell()

    output.tell("=" * 60)
    output.tell("FOUNDATION DEMO COMPLETE!")
    output.tell("=" * 60)
    output.tell()
    output.tell("Core systems tested:")
    output.tell("  ✓ Room creation and description")
    output.tell("  ✓ Container opening/closing")
    output.tell("  ✓ Item properties and flags")
    output.tell("  ✓ Light sources")
    output.tell("  ✓ Object movement and containment")
    output.tell("  ✓ Flag system (IntFlag enums)")
    output.tell()
    output.tell("Next steps: Parser, Game Engine, World Data")


if __name__ == "__main__":
    demo()

"""
Output formatting utilities for Zork I.

This module handles all text output to the player, including formatting,
word wrapping, and special text effects. Replaces the ZIL TELL macro and
related output functions.
"""

import sys
from typing import Any, Optional


class OutputManager:
    """
    Manages all game output to the player.

    This class provides utilities for formatted text output, replacing
    the ZIL TELL macro and related functions.
    """

    def __init__(self, width: int = 80):
        """
        Initialize the output manager.

        Args:
            width: Maximum line width for text wrapping
        """
        self.width = width
        self.buffer = []
        self.current_line_length = 0

    def tell(self, *args, **kwargs) -> None:
        """
        Output text to the player (replacement for ZIL TELL macro).

        This is the main output function. It handles various argument types:
        - Strings: printed directly
        - Objects with short_desc: prints description
        - 'D' followed by object: prints object description
        - 'CR' or newline: prints newline

        Args:
            *args: Variable arguments to output
            **kwargs: Optional 'end' parameter (default newline)
        """
        end = kwargs.get('end', '\n')

        output_parts = []
        i = 0

        while i < len(args):
            arg = args[i]

            # Handle special markers from ZIL TELL macro
            if isinstance(arg, str):
                if arg == 'CR' or arg == 'CRLF':
                    output_parts.append('\n')
                elif arg == 'D' and i + 1 < len(args):
                    # Description marker - print next arg's description
                    obj = args[i + 1]
                    output_parts.append(self._get_description(obj))
                    i += 1  # Skip next arg
                elif arg == 'A' or arg == 'AN' and i + 1 < len(args):
                    # Article marker - print "a" or "an" + description
                    obj = args[i + 1]
                    article = self._get_article(obj)
                    output_parts.append(f"{article} {self._get_description(obj)}")
                    i += 1
                elif arg == 'N' and i + 1 < len(args):
                    # Number marker
                    output_parts.append(str(args[i + 1]))
                    i += 1
                else:
                    output_parts.append(arg)
            elif hasattr(arg, 'short_desc'):
                # Object with description
                output_parts.append(self._get_description(arg))
            else:
                output_parts.append(str(arg))

            i += 1

        # Print the assembled output
        text = ''.join(output_parts)
        print(text, end=end)
        sys.stdout.flush()

    def _get_description(self, obj: Any) -> str:
        """
        Get the description of an object.

        Args:
            obj: Object to describe

        Returns:
            The object's short description or string representation
        """
        if hasattr(obj, 'short_desc'):
            return obj.short_desc
        elif hasattr(obj, 'desc'):
            return obj.desc
        else:
            return str(obj)

    def _get_article(self, obj: Any) -> str:
        """
        Get the appropriate article ("a" or "an") for an object.

        Args:
            obj: Object to get article for

        Returns:
            "a" or "an" depending on object name
        """
        desc = self._get_description(obj)
        if desc and desc[0].lower() in 'aeiou':
            return "an"
        return "a"

    def crlf(self) -> None:
        """Print a newline (replacement for ZIL CRLF)."""
        print()

    def prompt(self, text: str = ">") -> None:
        """
        Display the input prompt.

        Args:
            text: Prompt text to display
        """
        print(f"\n{text} ", end='')
        sys.stdout.flush()

    def clear_screen(self) -> None:
        """Clear the screen (platform-specific)."""
        # Simple implementation - could be enhanced for Windows
        print("\033[2J\033[H", end='')
        sys.stdout.flush()

    def print_score(self, score: int, moves: int, max_score: int = 350) -> None:
        """
        Print the score line.

        Args:
            score: Current score
            moves: Number of moves taken
            max_score: Maximum possible score
        """
        self.tell(f"Your score is {score} (out of {max_score}), in {moves} moves.")

    def print_room_header(self, room_name: str) -> None:
        """
        Print a room name header.

        Args:
            room_name: Name of the room
        """
        self.tell(f"{room_name}")

    def print_error(self, message: str) -> None:
        """
        Print an error message.

        Args:
            message: Error message to display
        """
        self.tell(message)

    def print_inventory(self, items: list) -> None:
        """
        Print inventory list.

        Args:
            items: List of items in inventory
        """
        if not items:
            self.tell("You are empty-handed.")
        else:
            self.tell("You are carrying:")
            for item in items:
                desc = self._get_description(item)
                self.tell(f"  {desc}")


# Global output manager instance
_output_manager: Optional[OutputManager] = None


def get_output_manager() -> OutputManager:
    """Get the global output manager instance."""
    global _output_manager
    if _output_manager is None:
        _output_manager = OutputManager()
    return _output_manager


def tell(*args, **kwargs) -> None:
    """
    Convenience function for outputting text.

    This is a shorthand for get_output_manager().tell()
    """
    get_output_manager().tell(*args, **kwargs)


def crlf() -> None:
    """Print a newline."""
    get_output_manager().crlf()

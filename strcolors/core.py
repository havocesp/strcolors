#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""strcolors core module.

 - File: strcolors/core.py
 - Author: Havocesp <https://github.com/havocesp/strcolors>
 - Created: 2022-11-12
 -
"""
import os
import platform
import re
import sys
from typing import Tuple

from strcolors.constants import *


class Term:
    """Term class."""

    # Set to False, to avoid colors and style methods like red() and bold() to just return formatted text without print to terminal.
    FLUSH = True

    @classmethod
    def _send(cls, cmd):
        """ Send command to terminal."""
        sys.stdout.write(cmd)
        sys.stdout.flush()

    @classmethod
    def pos(cls, line: int, column: int):
        """ Move cursor to supplied line (row) and column.

        :param line: line number.
        :param column: column number.
        """
        cls._send(f'\033[{line};{column}f')

    @classmethod
    def home_pos(cls):
        """ Move cursor to home position (line 1, column 1)."""
        cls._send('\033[H')

    @classmethod
    def up(cls, value=1):
        """ Move cursor up 'value' times.

        :param value: number of times to move cursor up.
        """
        cls._send(f'\033[{value}A')

    @classmethod
    def down(cls, value=1):
        """ Move cursor down 'value' times.

        :param value: number of times to move cursor down.
        """
        cls._send(f'\033[{value}B')

    @classmethod
    def right(cls, value=1):
        """ Move cursor right 'value' times.

        :param value: number of times to move cursor right.
        """
        cls._send(f'\033[{value}C')

    @classmethod
    def left(cls, value=1):
        """ Move cursor left 'value' times.

        :param value: number of times to move cursor left.
        """
        cls._send(f'\033[{value}D')

    @classmethod
    def save_cursor(cls):
        """ Save current cursor position."""
        cls._send('\0337')
        # TODO possible alternative: send('\033[s')

    @classmethod
    def restore_cursor(cls):
        """ Restore cursor position previously saved."""
        cls._send('\0338')
        # TODO possible alternative: send('\033[u')

    @classmethod
    def clear(cls):
        """ Clear screen."""
        cls._send('\033[2J')

    cls = clear

    @classmethod
    def clear_line_from_pos(cls):
        """ Clear line from cursor position to end of line."""
        cls._send('\033[K')

    @classmethod
    def clear_line_to_pos(cls):
        """ Clear line from line start to cursor position."""
        cls._send('\033[1K')

    @classmethod
    def clear_line(cls):
        """ Clear current line."""
        cls._send('\033[2K')

    @classmethod
    def print(cls, text: str = '', end='\n', *style):
        """ Print text after apply styles.

        :param text: text to print.
        :param end: end of line character.
        :param style: styles to applied to text.
        """
        cls._send(cls.fmt(f"{text}{end}", *style))

    @classmethod
    def set_title(cls, name):
        """ Set terminal title.

        :param name: title name.
        """
        cls._send(f'\033]2;{name}\007')

    @classmethod
    def set_tab(cls, name):
        """ Set tab name.

        :param name: tab name to be set.
        """
        cls._send(f'\033]1;{name}\007')

    @classmethod
    def strip(cls, text):
        """ Strip ANSI escape sequences from text. """
        return re.sub(r'\x1b\[[0-9]{1,2}m', '', text)

    @classmethod
    def center(cls, text):
        """Return a text aligned to center."""
        return ' ' * (int(cls.get_size()[1] / 2) - int(len(cls.strip(text)) / 2)) + text

    @classmethod
    def text_right(cls, text):
        """ Return a text aligned to right."""
        return ' ' * (cls.get_size()[1] - len(cls.strip(text))) + text

    @classmethod
    def get_size(cls, ) -> Tuple[int, int]:
        """ Get the size of the terminal.

        :return: a tuple with the number of rows and columns.
        """
        if any(platform.system().lower() in os_sys for os_sys in ('linux', 'darwin', 'cygwin')):
            try:
                def _get_unix_terminal_size(fd) -> Tuple:
                    from fcntl import ioctl
                    from termios import TIOCGWINSZ
                    from struct import unpack
                    return unpack('hh', ioctl(fd, TIOCGWINSZ, 'rene'))

                cr = _get_unix_terminal_size(0) or _get_unix_terminal_size(1) or _get_unix_terminal_size(2)
                if not cr:
                    with os.open(os.ctermid(), os.O_RDONLY) as term_id_fd:
                        cr = _get_unix_terminal_size(term_id_fd)
                return cr
            except Exception as err:
                print(f' - [ERROR] {err}', file=sys.stderr)
        else:
            raise OSError('Your system is not supported.')

    @classmethod
    def fmt(cls, text, *style):
        """ Format a text with the given style.

        :param text: the text to format.
        :param style: the style to apply.
        :return: the formatted text.
        """
        if style:
            return f'{"".join(style)}{text}{OFF}'
        else:
            return text

    @classmethod
    def highlight(cls, pattern, text, func):
        """ Highlight a pattern in a text with a function.

        :param pattern: regular expression pattern used to find the text b highlighted.
        :param text: text to highlight.
        :param func: a callable to apply to the pattern.
        :return: supplied text after applying the function to the pattern matches.
        """
        output = ''
        idx = 0
        matches = [(m.start(), m.end()) for m in re.finditer(pattern, text)]
        for p in matches:
            output += text[idx:p[0]]
            output += func(text[p[0]:p[1]])
            idx = p[1]
        output += text[idx:]
        return output, len(matches), matches

    @classmethod
    def red(cls, text: str) -> str:
        """ Return a red text. """
        return cls._send(cls.fmt(text, RED)) if cls.FLUSH else cls.fmt(RED)

    @classmethod
    def green(cls, text: str) -> str:
        """ Return a green text. """
        return cls._send(cls.fmt(text, GREEN)) if cls.FLUSH else cls.fmt(GREEN)

    @classmethod
    def yellow(cls, text: str) -> str:
        """ Return a yellow text. """
        return cls._send(cls.fmt(text, YELLOW)) if cls.FLUSH else cls.fmt(YELLOW)

    @classmethod
    def blue(cls, text: str) -> str:
        """ Return a blue text. """
        return cls._send(cls.fmt(text, BLUE)) if cls.FLUSH else cls.fmt(BLUE)

    @classmethod
    def magenta(cls, text: str) -> str:
        """ Return a magenta text. """
        return cls._send(cls.fmt(text, MAGENTA)) if cls.FLUSH else cls.fmt(MAGENTA)

    @classmethod
    def cyan(cls, text: str) -> str:
        """ Return a cyan text. """
        return cls._send(cls.fmt(text, CYAN)) if cls.FLUSH else cls.fmt(CYAN)

    @classmethod
    def white(cls, text: str) -> str:
        """ Return a white text. """
        return cls._send(cls.fmt(text, WHITE)) if cls.FLUSH else cls.fmt(WHITE)

    @classmethod
    def black(cls, text: str) -> str:
        """ Return a black text. """
        return cls._send(cls.fmt(text, BLACK)) if cls.FLUSH else cls.fmt(BLACK)

    @classmethod
    def underline(cls, text: str) -> str:
        """ Return a underlined text. """
        return cls._send(cls.fmt(text, UNDERSCORE)) if cls.FLUSH else cls.fmt(UNDERSCORE)

    @classmethod
    def blink(cls, text: str) -> str:
        """ Return a blinking text. """
        return cls._send(cls.fmt(text, BLINK)) if cls.FLUSH else cls.fmt(BLINK)

    @classmethod
    def reverse(cls, text: str) -> str:
        """ Return a reversed text. """
        return cls._send(cls.fmt(text, REVERSE)) if cls.FLUSH else cls.fmt(REVERSE)

    @classmethod
    def bg_red(cls, text: str) -> str:
        """ Return a red background text. """
        return cls._send(cls.fmt(text, BG_RED)) if cls.FLUSH else cls.fmt(BG_RED)

    @classmethod
    def bg_green(cls, text: str) -> str:
        """ Return a green background text. """
        return cls._send(cls.fmt(text, BG_GREEN)) if cls.FLUSH else cls.fmt(BG_GREEN)

    @classmethod
    def bg_yellow(cls, text: str) -> str:
        """ Return a yellow background text. """
        return cls._send(cls.fmt(text, BG_YELLOW)) if cls.FLUSH else cls.fmt(BG_YELLOW)

    @classmethod
    def bg_blue(cls, text: str) -> str:
        """ Return a blue background text. """
        return cls._send(cls.fmt(text, BG_BLUE)) if cls.FLUSH else cls.fmt(BG_BLUE)

    @classmethod
    def bg_magenta(cls, text: str) -> str:
        """ Return a magenta background text. """
        return cls._send(cls.fmt(text, BG_MAGENTA)) if cls.FLUSH else cls.fmt(BG_MAGENTA)

    @classmethod
    def bg_cyan(cls, text: str) -> str:
        """ Return a cyan background text. """
        return cls._send(cls.fmt(text, BG_CYAN)) if cls.FLUSH else cls.fmt(BG_CYAN)

    @classmethod
    def bg_white(cls, text: str) -> str:
        """ Return a white background text. """
        return cls._send(cls.fmt(text, BG_WHITE)) if cls.FLUSH else cls.fmt(BG_WHITE)

    @classmethod
    def bg_black(cls, text: str) -> str:
        """ Return a black background text. """
        return cls._send(cls.fmt(text, BG_BLACK)) if cls.FLUSH else cls.fmt(BG_BLACK)

    @classmethod
    def dim(cls, text: str) -> str:
        """ Return a dim text. """
        return cls._send(cls.fmt(text, DIM)) if cls.FLUSH else cls.fmt(DIM)

    @classmethod
    def bold(cls, text: str) -> str:
        """ Return a bold text. """
        return cls._send(cls.fmt(text, BOLD)) if cls.FLUSH else cls.fmt(text, BOLD)


# alias
Tm = Term

class ANSI:
    """ANSI escape codes for formatting text in a terminal."""

    class FG:
        """Foreground colors."""
        BLACK = "\033[30m"
        RED = "\033[31m"
        BOLD_RED = "\033[1;31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
        GREY = "\033[90m"
        RESET = "\033[39m"

    class BG:
        """Background colors."""
        BLACK = "\033[40m"
        RED = "\033[41m"
        BOLD_RED = "\033[1;41m"
        GREEN = "\033[42m"
        YELLOW = "\033[43m"
        BLUE = "\033[44m"
        MAGENTA = "\033[45m"
        CYAN = "\033[46m"
        WHITE = "\033[47m"
        GREY = "\033[100m"
        RESET = "\033[49m"

    class STYLE:
        """Text styles."""
        BOLD = "\033[1m"
        DIM = "\033[2m"
        UNDERLINE = "\033[4m"
        BLINK = "\033[5m"
        REVERSE = "\033[7m"
        HIDDEN = "\033[8m"
        RESET = "\033[0m"

    class RESET:
        """Reset all formatting."""
        ALL = "\033[0m"
        FOREGROUND = "\033[39m"
        BACKGROUND = "\033[49m"
        STYLE = "\033[0m"

    class CURSOR:
        """Cursor movement."""
        UP = "\033[1A"
        DOWN = "\033[1B"
        RIGHT = "\033[1C"
        LEFT = "\033[1D"
        SAVE = "\033[s"
        RESTORE = "\033[u"
        HIDE = "\033[?25l"
        SHOW = "\033[?25h"

    class ERASE:
        """Erase text."""
        SCREEN = "\033[2J"
        LINE = "\033[2K"
        END = "\033[K"
        START = "\033[1K"
        UP = "\033[1J"
        DOWN = "\033[1J"

    class SCROLL:
        """Scrolling."""
        UP = "\033D"
        DOWN = "\033M"
        LEFT = "\033H"
        RIGHT = "\033T"

    class WINDOW:
        """Window."""
        TITLE = "\033]0;"
        ICON = "\033]1;"
        RESET = "\007"

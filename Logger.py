# pylint: disable=line-too-long
# pylint: disable=dangerous-default-value
from enum import Enum
from typing import Callable
from datetime import datetime
import os


class Colors(Enum):
    """Colors for the terminal

    Args:
        Enum (str): All available ANSI formatting codes (some don't work)

    Returns:
        str: The ANSI formatting code
    """
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    SLOW_BLINK = '\033[5m'
    REVERSE = '\033[7m'
    CONCEAL = '\033[8m'
    CROSSED_OUT = '\033[9m'
    REVEAL = '\033[28m'
    FRAMED = '\033[51m'  # doesn't work
    ENCIRCLED = '\033[52m'
    OVERLINED = '\033[53m'  # doesn't work
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

    @classmethod
    def from_rgb(cls, red: int, green: int, blue: int) -> str:
        """Returns the ANSI formatting code for the given RGB color

        Args:
            red (int): The red value for the color (0-255)
            green (int): The green value for the color (0-255)
            blue (int): The blue value for the color (0-255)

        Returns:
            str: The ANSI formatting code for the color
        """
        return f"\033[38;2;{red};{green};{blue}m"


class FileHandler:

    def __init__(self, loc: str = ""):
        self.loc = loc
        directory = loc.split("/")
        del directory[-1]
        self.directory = "".join([f"{path}/" for path in directory])

    def save(self, content: str):
        self.create_and_append(content, self.loc)

    def create_and_append(self, content: str, loc: str):
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        with open(loc, "a+") as f:
            f.write(content + "\n")
            f.close()


class Logger:
    class Level(Enum):
        """The level of the log message

        Args:
            Enum (int): The number of the level
        """
        DEBUG = 0
        LOG = 1
        INFO = 2
        WARNING = 3
        ERROR = 4

    # Default colors for the different levels
    __default_colors = {
        "DEBUG": Colors.WHITE.value,
        "LOG": "",
        "INFO": Colors.GREEN.value,
        "WARNING": Colors.YELLOW.value,
        "ERROR": Colors.RED.value
    }

    @staticmethod
    def get_default_colors() -> dict:
        return Logger.__default_colors.copy()

    @staticmethod
    def default_formatter(text, level: Level = Level.INFO, name: str = __name__,
                          colors: dict = __default_colors) -> str:
        """The default log formatter

        Args:
            text (any): The text to log
            level (Level, optional): The Level to use for logging. Defaults to Level.INFO.
            name (str, optional): The name for the current logger. Defaults to __name__.

        Returns:
            str: The formatted string for printing to the console
        """
        return f"{name} - {level.name}: {colors.get(level.name, '')}{str(text)}"

    @staticmethod
    def minecraft_formatter(text, level: Level = Level.INFO, name: str = __name__,
                            colors: dict = __default_colors) -> str:
        """The default log formatter for Minecraft

        Args:
            text (any): The text to log
            level (Level, optional): The Level to use for logging. Defaults to Level.INFO.
            name (str, optional): The name for the current logger. Defaults to __name__.

        Returns:
            str: The formatted string for printing to the console
        """
        return f"[{str(datetime.now().time()).split('.')[0]}] [{name}]: [{level.name}] {colors.get(level.name, '')}{str(text)}"

    def __init__(self, name: str = __name__, level: Level = Level.INFO,
                 formatter: Callable[[str, Level, str, dict], str] = default_formatter,
                 level_colors: dict = __default_colors, fh: FileHandler = None):
        """A simple logger with color support and logging levels

        Args:
            name (str, optional): The name to use for the logger. Defaults to __name__.
            level (Level, optional): The lowest level to print to the console. Defaults to Level.INFO.
            formatter (Callable[[str, Level, str], str], optional): The formatter that returns a prettified string for logging. Defaults to default_formatter.
            level_colors (dict, optional): The colors to use for each level. Defaults to default_colors.
        """
        self.name = name
        self.formatter = formatter
        self.level = level
        self.colors = level_colors
        self.fh = fh

    def format_text(self, text: str, level: Level):
        return f"{self.formatter(str(text), level, self.name, self.colors)}{Colors.RESET.value}"

    def log(self, text="", level: Level = Level.LOG):
        """Logs the given text to the console

        Args:
            text (any): The text to log
            level (Level, optional): The level to use for logging. Defaults to Level.LOG.
        """
        formatted = self.format_text(text, level)
        if self.level.value <= level.value:
            print(formatted)
            self.fh.save(formatted)

        if level == Logger.Level.ERROR and self.fh is not None:
            self.fh.create_and_append(formatted, f"{self.fh.directory}/error.log")

    def debug(self, text=""):
        """Logs a message at the Level.DEBUG level

        Args:
            text (any): The text to log
        """
        self.log(text, Logger.Level.DEBUG)

    def info(self, text=""):
        """Logs a message at the Level.INFO level

        Args:
            text (any): The text to log
        """
        self.log(text, Logger.Level.INFO)

    def warning(self, text=""):
        """Logs a message at the Level.WARNING level

        Args:
            text (any): The text to log
        """
        self.log(text, Logger.Level.WARNING)

    def error(self, text=""):
        """Logs a message at the Level.ERROR level

        Args:
            text (any): The text to log
        """
        self.log(text, Logger.Level.ERROR)


# Testing
if __name__ == "__main__":



    lg = Logger("Logger Test", level=Logger.Level.LOG, formatter=Logger.minecraft_formatter, fh=FileHandler("./logs/log.log"))

    for color in Colors:
        lg.log(f"{color.value}{color.name}")

    lg.log()
    lg.log()

    lg.debug("This won't get printed!")
    lg.info("This is an information!")
    lg.error(f"{Colors.ENCIRCLED.value}This is an error!")
    lg.error(f"{Colors.from_rgb(20, 100, 100)}This is an error with a color created from rgb")

"""
Models related to the game's state.
"""
from enum import Enum
from datetime import datetime

from util import count_adjacent_mines


class GameStatus(Enum):
    """
    Possible statuses for the game. There is no "not running" status,
    because we can always assume that the game is either running or
    has ended when the game window is open.
    """
    RUNNING = 1
    LOST = 2
    WON = 3

    def __bool__(self):
        return self != GameStatus.RUNNING


class TileState:
    """
    State of a tile. Much cleaner than storing the tiles as strings.
    """
    opened = False
    mined = False
    flagged = False

    def __init__(self, state, pos: tuple):
        self.state = state
        self.pos = pos

    def sprite(self) -> str:
        """
        Returns the key of this tile's sprite.

        :return: The key
        """
        if self.state.game_status and self.mined:
            return "x"

        if self.opened:
            return str(count_adjacent_mines(self.pos[0], self.pos[1], self.state))

        if self.flagged:
            return "f"

        return " "


class SweeperState:
    """
    State of the game. This could have been done with a dictionary, but I much prefer this
    since it allows the IDE to inspect the code better.
    """
    field = []
    game_status = GameStatus.RUNNING
    mined = False
    mines = 100
    begin_time = datetime.now()
    opened = 0

    def height(self) -> int:
        """
        Calculates the height of the field.

        :return: Height of the field.
        """
        return len(self.field)

    def width(self) -> int:
        """
        Calculates the width of the field.

        :return: Width of the field.
        """
        return len(self.field[0])

    def tile_at(self, x: int, y: int) -> TileState:
        """
        Returns the tile at certain coordinates.

        :param x: X coordinate of the tile.
        :param y: Y coordinate of the tile.
        :return: The tile
        """
        return self.field[y][x]

    def init_field(self, width, height) -> None:
        """
        Initializes the field with provided values. The field won't contain any mines until the
        first tile is opened, since the first tile opened should never contain a mine.

        :param width: Width of the field
        :param height: Height of the field
        """
        self.begin_time = datetime.now()

        for y in range(height):
            row = []

            for x in range(width):
                row.append(TileState(self, (x, y)))

            self.field.append(row)

    def is_in_bounds(self, x: int, y: int) -> bool:
        """
        Checks whether the tile in provided coordinates is in bounds.

        :param x: X coordinate of the tile.
        :param y: Y coordinate of the tile.
        :return: Whether the tile is in bounds
        """
        return 0 <= y < len(self.field) and 0 <= x < len(self.field[0])

    def count_remaining(self) -> int:
        """
        Count remaining unopened, unmined tiles.

        :return: Amount of unopened, unmined tiles.
        """
        c = 0

        for r in self.field:
            for tile in r:
                if not tile.mined and not tile.opened:
                    c += 1

        return c

    def reset(self) -> None:
        """
        Resets all properties of this object.
        """
        self.field = []
        self.game_status = GameStatus.RUNNING
        self.mined = False
        self.mines = 100
        self.begin_time = datetime.now()
        self.opened = 0

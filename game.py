"""
Logic for the minestomper game.
"""
from datetime import datetime
import random

import sweeperlib
import stats
from state import SweeperState, GameStatus
from util import open_floodfill

state = SweeperState()


def place_mines(tiles: list, amount: int) -> None:
    """
    Places N mines to a field in random tiles.

    :param tiles: list of tuples with possible tile coordinates.
    :param amount: amount of mines to be placed
    """
    random.shuffle(tiles)

    for _ in range(amount):
        tile = tiles.pop(0)

        state.tile_at(tile[0], tile[1]).mined = True


def setup_field(x: int, y: int) -> None:
    """
    Populates the field with mines. The parameters define a tile that is always left empty.

    :param x: X coordinate of the always empty tile
    :param y: Y coordinate of the always empty tile
    """
    tiles = []

    for i in range(state.height()):
        for j in range(state.width()):
            if j == x and i == y:
                continue

            tiles.append((j, i))

    place_mines(tiles, state.mines)
    state.mined = True


def open_tile(x: int, y: int) -> None:
    """
    Logic for opening a tile. If the field is yet to be mined,
    this function will mine it and leave the clicked tile empty.
    This way the first opened tile will never contain a mine.

    :param x: X coordinate of the opened tile
    :param y: Y coordinate of the opened tile
    :return:
    """
    if not state.mined:
        setup_field(x, y)

    tile = state.tile_at(x, y)

    if tile.flagged:
        return

    state.opened += 1

    if tile.mined:
        state.game_status = GameStatus.LOST
        end()
        return

    open_floodfill(state, x, y)

    if state.count_remaining() == 0:
        state.game_status = GameStatus.WON
        end()


def flag_tile(x: int, y: int) -> None:
    """
    Logic for placing or removing flag for a tile. A flagged tile cannot be opened
    without removing the flag first.

    :param x: X coordinate of the tile
    :param y: Y coordinate of the tile
    """
    if state.game_status:
        return

    tile = state.tile_at(x, y)

    if tile.opened:
        return

    tile.flagged = not tile.flagged


def end() -> None:
    """
    Performs ending logic.
    """
    save_current()


def save_current() -> None:
    """
    Saves stats for current game.
    """
    stats.add_statistic(state.begin_time, datetime.now(), state.opened, state.game_status == GameStatus.WON,
                        state.width(), state.height(), state.mines)


def draw_field():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """
    field = state.field

    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()

    for y in range(len(field)):
        for x in range(len(field[0])):
            sweeperlib.prepare_sprite(field[y][x].sprite(), x * 40, y * 40)

    sweeperlib.draw_sprites()


def handle_mouse(x, y, button, mod):
    """
    This function is called when a mouse button is clicked inside the game window.
    Prints the position and clicked button of the mouse to the terminal.
    """
    if state.game_status or not state.is_in_bounds(x // 40, y // 40):
        return

    if button == sweeperlib.MOUSE_LEFT:
        open_tile(x // 40, y // 40)

    if button == sweeperlib.MOUSE_RIGHT:
        flag_tile(x // 40, y // 40)


def main(mines=5, width=8, height=8) -> None:
    """
    Loads the game graphics and starts the game.
    """

    state.mines = mines
    state.init_field(width, height)

    sweeperlib.load_sprites("./sprites/")
    sweeperlib.create_window(width * 40, height * 40)
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.set_mouse_handler(handle_mouse)
    sweeperlib.start()


if __name__ == '__main__':
    main()

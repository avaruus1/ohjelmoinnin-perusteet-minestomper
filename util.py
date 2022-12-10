"""
Utility functions for the game.
"""


def count_adjacent_mines(col, row, state):
    """
    Counts the mines surrounding a tile. The function assumes the selected tile does
    not have a mine in it - if it does, it counts that one as well.
    """

    count = 0

    for y in range(row - 1, row + 2):
        for x in range(col - 1, col + 2):
            if x == col and y == row:
                continue
            if x < 0 or y < 0 or y >= state.height() or x >= state.width():
                continue

            if state.field[y][x].mined:
                count += 1

    return count


def find_empty_adjacent(col, row, state):
    """
    Find empty tiles surrounding a tile.
    """
    empty = []

    for y in range(row - 1, row + 2):
        for x in range(col - 1, col + 2):
            if x == col and y == row:
                continue
            if x < 0 or y < 0 or y >= state.height() or x >= state.width():
                continue

            tile = state.tile_at(x, y)

            if not tile.mined and not tile.opened:
                empty.append((x, y))

    return empty


def open_floodfill(state, x, y):
    """
    Opens empty tiles until a number tile is reached.
    """
    if state.tile_at(x, y).mined:
        return

    tiles = [(x, y)]

    while tiles:
        x, y = tiles.pop()

        state.tile_at(x, y).opened = True

        if count_adjacent_mines(x, y, state) > 0:
            continue

        tiles.extend(find_empty_adjacent(x, y, state))

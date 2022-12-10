"""
Module for statistics. By default, stats are saved in a stats.json file in the running directory.
"""
import json
from datetime import datetime

DEFAULT_STATS_FILE = "stats.json"

stats = []


def add_statistic(begin_time: datetime, end_time: datetime, tiles_opened: int, win: bool, field_width: int,
                  field_height: int, mine_amount: int) -> None:
    """
    Save statistic & write everything to the default file.

    :param begin_time: The time this game began
    :param end_time: The times this game ended
    :param tiles_opened: Tiles the player opened. Tiles opened by floodfill don't count. i.e. amount of turns.
    :param win: Whether the game was a win.
    :param field_width: Width of the field.
    :param field_height: Height of the field.
    :param mine_amount: Amount of mines in the field
    """

    stats.append({
        "begin_time": begin_time.isoformat(),
        "end_time": end_time.isoformat(),
        "tiles_opened": tiles_opened,
        "win": win,
        "field_width": field_width,
        "field_height": field_height,
        "mine_amount": mine_amount
    })

    write(DEFAULT_STATS_FILE)


def print_stats() -> None:
    """
    Print stats to console. (In a pretty format!)
    """
    if len(stats) == 0:
        print("Tallennettuja tilastoja ei löytynyt.")
        return

    format_str = "{:<28} | {:<12} | {:<8} | {:<8} | {:<16} | {:<8}"

    print(format_str.format("Alkamisaika", "Kesto (min)", "Vuorot", "Voitto", "Kenttä (W x H)", "Miinojen lkm"))

    for stat in stats:
        delta = (datetime.fromisoformat(stat["end_time"]) - datetime.fromisoformat(stat["begin_time"]))

        print(format_str.format(
            stat["begin_time"],
            f"{delta.total_seconds() / 60:.2f}",
            stat["tiles_opened"],
            "Kyllä" if stat["win"] else "Ei",
            f"{stat['field_width']} x {stat['field_height']}",
            stat["mine_amount"]
        ))


def write(file_name: str) -> None:
    """
    Write stats to file.

    :param file_name: Path to the file.
    """
    with open(file_name, "w") as file:
        file.write(json.dumps(stats, indent=2))


def read(file_name: str) -> None:
    """
    Read stats from the file.

    :param file_name: Path to the file
    """
    try:
        with open(file_name) as file:
            data = json.load(file)

            stats.clear()

            for datum in data:
                stats.append(datum)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Exception while reading {file_name}. It'll be overriden next time stats are saved.")


read(DEFAULT_STATS_FILE)

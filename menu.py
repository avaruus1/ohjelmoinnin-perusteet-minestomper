"""
Menu module contains the code for the main menu. It should be opened via the open_menu function.
"""
import game
import stats


def request_int(prompt: str, bounds_min=None, bounds_max=None) -> int:
    """
    Prompts the user for an integer. Doesn't give up until the user gives a valid one.

    :param prompt: Prompt for input
    :param bounds_min: Lower bound for the value. None for unrestricted.
    :param bounds_max: Upper bound for the value. None for unrestricted.
    :return: The requested integer
    """
    while True:
        try:
            i = int(input(prompt))

            if bounds_min is not None and bounds_min >= i:
                print(f"Luvun tulee olla suurempi kuin {bounds_min}")
                continue

            if bounds_max is not None and bounds_max <= i:
                print(f"Luvun tulee olla pienempi kuin {bounds_max}")
                continue

            return i
        except ValueError:
            print("Tuo ei ollut kokonaisluku, yritä uudelleen.")


def menu_play() -> bool:
    """
    Prompts the user questions regarding the game options & starts the game with acquired options.

    :return: False, to not terminate the program
    """
    height = request_int("Syötä kentän korkeus: ", 0)
    width = request_int("Syötä kentän leveys: ", 0)
    mines = request_int("Syötä miinojen määrä: ", 0, height * width)

    game.main(mines, width, height)

    game.state.reset()

    return False


def menu_stats() -> bool:
    """
    Displays statistics to the user.

    :return: False, to not terminate the program.
    """
    stats.print_stats()

    return False


def menu_quit() -> bool:
    """
    Terminates the program.

    :return: True, to terminate the program.
    """
    print("Heippa")

    return True


MENU_OPTIONS = {
    **dict.fromkeys(["play", "pelaa", "p"], menu_play),
    **dict.fromkeys(["stats", "tilastot", "s"], menu_stats),
    **dict.fromkeys(["quit", "poistu", "q"], menu_quit)
}


def open_menu() -> None:
    """
    Opens the game menu.
    """
    while True:
        print("Toiminnot: pelaa (p) | tilastot (s) | poistu (q)")

        try:
            if MENU_OPTIONS[input("Valinta: ").lower()]():
                break
        except KeyError:
            print("Virheellinen valinta")

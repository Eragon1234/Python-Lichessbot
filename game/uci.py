from game.types import Coordinate, Move

index_to_letter = ord("a")


def uci_string_into_coordinate(uci_string: str) -> Coordinate:
    """ converts a coordinate string into a coordinate tuple

    Args:
        uci_string (str): a string containing the coordinates

    Returns:
        tuple: a tuple containing the coordinates
    """
    x = ord(uci_string[0]) - index_to_letter
    y = int(uci_string[1]) - 1
    return x, y


def coordinate_into_uci_string(coordinate: Coordinate) -> str:
    """ converts a coordinate tuple into a coordinate string

    Args:
        coordinate (tuple): a tuple containing the coordinates

    Returns:
        str: a string containing the coordinates
    """
    x = chr(coordinate[0] + index_to_letter)
    y = coordinate[1] + 1
    return f"{x}{y}"


def coordinate_move_into_uci(coordinate_move: Move) -> str:
    """ converts the passed coordinate move into an UCI move

    Args:
        coordinate_move (tuple): a tuple containing the startField and the targetField as x, y tuples

    Returns:
        list: a list containing the startField and the targetField as x, y tuples
    """
    start_field = coordinate_into_uci_string(coordinate_move[0])
    target_field = coordinate_into_uci_string(coordinate_move[1])
    return f"{start_field}{target_field}"


def uci_into_coordinate_move(uci_move: str) -> Move:
    """ converts the passed UCIMove into a coordinate move

    Args:
        uci_move (string): the UCIMove to convert into an UCIMove

    Returns:
        tuple: the coordinate move corresponding to the passed UCIMove
    """
    start_field = uci_string_into_coordinate(uci_move[:2])
    target_field = uci_string_into_coordinate(uci_move[2:])
    return start_field, target_field

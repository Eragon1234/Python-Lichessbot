index_to_letter = ord("a")


def coordinate_string_into_coordinate(coordinate_string: str) -> tuple[int, int]:
    """ converts a coordinate string into a coordinate tuple

    Args:
        coordinate_string (str): a string containing the coordinates

    Returns:
        tuple: a tuple containing the coordinates
    """
    x = ord(coordinate_string[0]) - index_to_letter
    y = int(coordinate_string[1]) - 1
    return x, y


def coordinate_into_coordinate_string(coordinate: tuple[int, int]) -> str:
    """ converts a coordinate tuple into a coordinate string

    Args:
        coordinate (tuple): a tuple containing the coordinates

    Returns:
        str: a string containing the coordinates
    """
    x = chr(coordinate[0] + index_to_letter)
    y = coordinate[1] + 1
    return f"{x}{y}"


def coordinate_move_into_uci(coordinate_move: tuple[tuple[int, int], tuple[int, int]]) -> str:
    """ converts the passed coordinate move into an UCI move

    Args:
        coordinate_move (tuple): a tuple containing the startField and the targetField as x, y tuples

    Returns:
        list: a list containing the startField and the targetField as x, y tuples
    """
    start_field = coordinate_into_coordinate_string(coordinate_move[0])
    target_field = coordinate_into_coordinate_string(coordinate_move[1])
    return f"{start_field}{target_field}"


def coordinate_moves_into_uci(coordinate_moves: list[tuple[tuple[int, int], tuple[int, int]]]) -> list[
    str]:
    """ converts the passed array of coordinate moves into an array of UCIMoves

    Args:
        coordinate_moves (list): a list containing tuples with the startField and the targetField as x, y tuples

    Returns:
        list: a list of strings which are moves in the UCI Notation
    """
    moves = []
    for coordinateMove in coordinate_moves:
        moves.append(coordinate_move_into_uci(coordinateMove))
    return moves


def uci_into_coordinate_move(uci_move: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """ converts the passed UCIMove into a coordinate move

    Args:
        uci_move (string): the UCIMove to convert into an UCIMove

    Returns:
        tuple: the coordinate move corresponding to the passed UCIMove
    """
    start_field = coordinate_string_into_coordinate(uci_move[:2])
    target_field = coordinate_string_into_coordinate(uci_move[2:])
    return start_field, target_field

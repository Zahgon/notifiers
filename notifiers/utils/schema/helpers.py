from __future__ import annotations


def one_or_more(schema: dict, unique_items: bool = True, min: int = 1, max: int | None = None) -> dict:
    """
    Helper function to construct a schema that validates items matching
    `schema` or an array containing items matching `schema`.

    :param schema: The schema to use
    :param unique_items: Flag if array items should be unique
    :param min: Correlates to ``minLength`` attribute of JSON Schema array
    :param max: Correlates to ``maxLength`` attribute of JSON Schema array
    """
    pass


def list_to_commas(list_of_args) -> str:
    """
    Converts a list of items to a comma separated list. If ``list_of_args`` is
    not a list, just return it back

    :param list_of_args: List of items
    :return: A string representing a comma separated list.
    """
    pass
    # todo change or create a new util that handle conversion to list as well

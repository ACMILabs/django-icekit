import string

ALPHABET = string.digits + string.lowercase

def base36encode(number):
    """Converts a positive integer to a base36 string."""
    if not isinstance(number, (int, long)):
        raise TypeError('`number` must be an integer')

    base36 = ''

    if 0 <= number < len(ALPHABET):
        return ALPHABET[number]

    while number != 0:
        number, i = divmod(number, len(ALPHABET))
        base36 = ALPHABET[i] + base36

    return base36


def base36decode(number):
    return int(number, len(ALPHABET))


def short_code_from_id(integer, min_length=2):
    """
    :param input: a positive integer (ID) representing the URL to be shortened.
    :return: a string comprising the letters 0-9 and a-z that maps to that ID

    Assuming a DB ID is passed, the result should be unique.

    We will also ensure that the returned string is at least n characters long, so that the single-character namespace
    is reserved for future. We do this by adding len(ALPHABET) ^ min_length to the integer.

    It's not necessary that this function be reversible - as we're using a database lookup - just unique. (If we needed
    reversibility we'd either need to fix min_length or would need to encode it in the output.)
    """

    minimum_number = len(ALPHABET) ** (min_length - 1)
    return base36encode(integer + minimum_number)

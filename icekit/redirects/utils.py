ALPHABET = "23456789abcdefghjkmnpqrstuvxyz" # removing ambiguous chars, and w, which is used to deprofane.

# from https://stackoverflow.com/questions/3531746/what-s-a-good-python-profanity-filter-library
# not including words that have chars that don't appear above. Replace the first character with 'w' to sacredify.
PROFANITY = ['ass', 'cum', 'cunt', 'fuc', 'fuk', 'bj', 'nud', 'puss', 'rape', 'scat', 'sex',]
CLEANED = [(p, 'w' + p[1:]) for p in PROFANITY]

def baseXencode(number):
    """Converts a positive integer to a baseX string."""
    if not isinstance(number, (int, long)):
        raise TypeError('`number` must be an integer')

    baseX = ''

    if 0 <= number < len(ALPHABET):
        return ALPHABET[number]

    while number != 0:
        number, i = divmod(number, len(ALPHABET))
        baseX = ALPHABET[i] + baseX

    for p, q in CLEANED:
        baseX = baseX.replace(p, q)

    return baseX


# def baseXdecode(number):
#     """
#     NOTE: this isn't used or working, but is provided as a starting point.
#
#     TODO: subtract `mininmum_number` from the output.
#
#     TODO: Due to the profanity filter, inputs involving 'w' will need to be back-converted to the
#     profane version.
#     """
#     return int(number, len(ALPHABET))


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
    return baseXencode(integer + minimum_number)

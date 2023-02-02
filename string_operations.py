""" Common utility procedures for strings manipulation.

@author Provotorov A. merqcio11@gmail.com
"""


def strcmp(str1:str, str2:str, ignore_case: bool = False):
    """Compare strings in specified way.
    """
    s1 = str1.casefold() if ignore_case else str1
    s2 = str2.casefold() if ignore_case else str2
    return s1 == s2

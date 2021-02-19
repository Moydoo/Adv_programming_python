
from lev_1 import Levenshtein

PUNCTATION_MARKS = ['.', ',', ':', ';']


class WordsComparison:
    first = ""
    second = ""
    distance = 0

    def __init__(self, first, second, distance):
        self.first = first
        self.second = second
        self.distance = distance

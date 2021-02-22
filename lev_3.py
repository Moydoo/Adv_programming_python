from lev_1 import Levenshtein
from freq import FrequencyList, PUNCTATION_MARKS
# tqdm libka do fajnego wyswietlania iteracji w petli
from tqdm import tqdm

freq = FrequencyList("wiki.txt")


class WordsComparison:
    first = ""
    second = ""
    distance = 0
    frequency = 0
    double_frequency = 0

    def __init__(self, first, second, distance, frequency, double_frequency):
        self.first = first
        self.second = second
        self.distance = distance
        self.frequency = frequency
        self.double_frequency = double_frequency


def fix_sentence(sentence, dictionary, levenstein: Levenshtein):
    sort_key = lambda x: x.distance
    sort_key_freq_weight = lambda x: (x.frequency*0.5 + x.double_frequency)

    for mark in PUNCTATION_MARKS:
        sentence = sentence.replace(mark, '')
    words = sentence.split(' ')
    distances = {}
    for i, w in enumerate(words):
        lower_word = w.lower()
        if lower_word in dictionary:
            distances[w] = []
        else:
            comparisons = []
            for dic_word in tqdm(dictionary):
                if i < len(words) - 1:
                    double_n_gram_freq = freq.get_bi_gram_frequency(dic_word, words[i + 1])
                else:
                    double_n_gram_freq = 0
                comparisons.append(
                    WordsComparison(
                        lower_word,
                        dic_word,
                        levenstein(w, dic_word)[0],
                        freq.get_n_gram_frequency(dic_word),
                        double_n_gram_freq
                    )
                )
            # sort by levenstein distance
            comparisons.sort(key=sort_key)
            # get best 10 propositions (levenstein value)
            distances[w] = comparisons[:10]

        if distances[w]:
            print(f"Best replacements for word \"{w}\": "
                  f"{[str(f'(word: {r.second}, distance: {r.distance}, n_gram_frequency: {r.frequency}, double_n_gram_frequency: {r.double_frequency})', ) for r in distances[w]]} \n")
    proposition = ""
    for key, best_values in distances.items():
        if not best_values:
            proposition += key + ' '
        else:
            # liczymy srednią ważoną ilości frekwencji: frekwencja wystepowania pojedynczego słowa
            # (n_gram_frequency) * 0.5 i frekwencja występowania słowa w parze z innym (double_n_gram_frequency) * 1.0
            # n_gram_frequency * 0.5 + double_n_gram_frequency * 1.0 -> w wtedy sortujemy i wybieramy najlepsze

            best_values.sort(key=sort_key_freq_weight, reverse=True)
            proposition += best_values[0].second + ' '

    return proposition[:-1]


if __name__ == "__main__":
    lev = Levenshtein()

    # dictionary load
    sjp = [word.replace('\n', '').lower() for word in open("sjp.txt", encoding="utf-8").readlines()]

    # hardcoded sentences
    sentences = ["Mój muzg dużo to nażąd szczątkowy"]
    print(sentences[0])
    for s in sentences:
        prop = fix_sentence(s, sjp, lev)
        if s != prop:
            print(f"There is a mistake in: \"{s}\", it should be: \"{prop}\"")
        else:
            print(f"There is no mistake: \"{s}\"")


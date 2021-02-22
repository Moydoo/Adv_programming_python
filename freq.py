
PUNCTATION_MARKS = ['.', ',', ':', ';', '(', ')', '-', '?', '!']


class FrequencyList:

    def __init__(self, dic):
        self._dictionary = open(dic, encoding = "utf-8").read().split()
        self.remove_punctation_marks(self._dictionary)
        self._n_gram_freq = self.get_n_gram_frequency_dic(self._dictionary)
        self._bi_gram_freq = self.get_double_n_gram_frequency_dic(self._dictionary)

    def get_n_gram_frequency(self, word):
        return 0 if word not in self._n_gram_freq.keys() else self._n_gram_freq[word]

    def get_bi_gram_frequency(self, word1, word2):
        words = (word1, word2)
        return 0 if words not in self._bi_gram_freq.keys() else self._bi_gram_freq[words]

    @staticmethod
    def remove_punctation_marks(dic):
        for i, word in enumerate(dic):
            for mark in PUNCTATION_MARKS:
                if mark in word:
                    dic[i] = word.replace(mark, '')

    @staticmethod
    def remove_not_words(dic):
        new_dic = []
        for word in dic:
            if word.isalpha():
                new_dic.append(word)
        return new_dic

    @staticmethod
    def get_n_gram_frequency_dic(dic):
        freq_dic = {}
        for word in dic:
            if word in freq_dic.keys():
                freq_dic[word] += 1
            else:
                freq_dic[word] = 1
        return freq_dic

    @staticmethod
    def get_double_n_gram_frequency_dic(dic):
        freq_double_n_gram_dic = {}
        for i in range(len(dic) - 1):
            tup_words = (dic[i], dic[i + 1])
            if tup_words in freq_double_n_gram_dic:
                freq_double_n_gram_dic[tup_words] += 1
            else:
                freq_double_n_gram_dic[tup_words] = 1
        return freq_double_n_gram_dic


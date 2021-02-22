class Levenshtein:

    diacritic_sign = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż']
    normal_sign = ['a', 'c', 'e', 'l', 'n', 'o', 's', 'z', 'z']
    edge_cases = [('u', 'ó')]
    double_edge_cases = [('ch', 'h'), ('rz', 'ż')]

    def __call__(self, w1, w2):
        """
        Call function to calculate levenshtein and weights
        :param w1: first word
        :param w1: second word
        :return: tuple of levenshtein value and weight of error
        """
        table = []
        weights = []
        word1_length, word2_length = len(w1), len(w2)
        for x in range(word1_length + 1):
            table.append([x] + list(range(1, word2_length + 1)))
            weights.append([x] + list(range(1, word2_length + 1)))

        for i in range(word1_length):
            for j in range(word2_length):
                first_edge_case = [e[0] for e in self.edge_cases]
                second_edge_case = [e[1] for e in self.edge_cases]
                first_double_edge_case = [e[0] for e in self.double_edge_cases]
                second_double_edge_case = [e[1] for e in self.double_edge_cases]
                double_exist = False
                if w1[i] == w2[j]:
                    check = table[i][j]
                    fail_sign = weights[i][j]
                elif self.error_occurs(w1[i], w2[j], self.diacritic_sign, self.normal_sign):
                    fail_sign = weights[i][j] + 0.2
                    check = table[i][j] + 1
                elif self.error_occurs(w1[i], w2[j], first_edge_case, second_edge_case):
                    fail_sign = weights[i][j] + 0.5
                    check = table[i][j] + 1
                elif (j + 1 < word2_length and self.error_occurs(w2[j:j + 2], w1[i], first_double_edge_case,
                                                            second_double_edge_case)) or (
                        i + 1 < word1_length and self.error_occurs(w1[i:i + 2], w2[j], first_double_edge_case,
                                                              second_double_edge_case)):
                    fail_sign = weights[i][j] + 0.5
                    check = table[i][j] + 1
                    double_exist = True
                elif i + 1 < word1_length and j + 1 < word2_length and w1[i] == w2[j + 1] and w2[j] == w1[i + 1]:
                    fail_sign = weights[i][j] - 0.5
                    check = table[i][j] + 1
                else:
                    check = table[i][j] + 1
                    fail_sign = weights[i][j] + 1

                weights[i + 1][j + 1] = self.set_next_value(fail_sign, weights, i, j)
                table[i + 1][j + 1] = self.set_next_value(check, table, i, j)

                if double_exist:
                    weights[i + 1][j + 1] -= 1
                    table[i + 1][j + 1] -= 1

        return table[-1][-1], weights[-1][-1]

    @staticmethod
    def set_next_value(reference, values_set, incr1, incr2):
        return min(reference, values_set[incr1][incr2 + 1] + 1, values_set[incr1 + 1][incr2] + 1)

    @staticmethod
    def error_occurs(val1, val2, set1, set2):
        return (val1 in set1 and val2 in set2 and set1.index(val1) == set2.index(val2)) or (
                val1 in set2 and val2 in set1 and set1.index(val2) == set2.index(val1))


if __name__ == "__main__":
    test_list_2 = [('śmiech', 'smiech'), ('pierze', 'pieże'), ('huśtawka', 'chóśtawka'), ('zrobić', 'rzobić'),
                   ('człowiek', 'cłzoiwek'), ('prosiłem', 'prsoilem')]
    levenshtein = Levenshtein()
    for pair in test_list_2:
        lev_distance, lev_weight = levenshtein(pair[0], pair[1])
        print(f"Weight value for {pair} = {lev_weight}")

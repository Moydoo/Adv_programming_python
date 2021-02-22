def lev(w1, w2):
    table = []
    word1_length, word2_length = len(w1), len(w2)
    for x in range(word1_length + 1):
        table.append([x] + list(range(1, word2_length + 1)))

    for i in range(word1_length):
        for j in range(word2_length):
            check = table[i][j] + 0 if w1[i] == w2[j] else table[i][j] + 1
            table[i + 1][j + 1] = min(check, table[i][j + 1] + 1, table[i + 1][j] + 1)
    return table[-1][-1]


if __name__ == "__main__":#w sumie tutaj to nie jest potrzebne, ale już kij 
    test_list = [('pies', 'pies'), ('granat', 'granit'), ('orczyk', 'oracz'), ('marka', 'ariada')]
    for pair in test_list:
        print(f"Levenshtein value for {pair} = {lev(pair[0], pair[1])}")

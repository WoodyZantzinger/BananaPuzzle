

scrabble_values = [-1, 3, 3, 2, -1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]

def scoreWord(word):
    length = len(word)
    total_score = 0

    for letter in word:
        total_score += scrabble_values[ord(letter) - 97]

    return total_score / length


def print_letters(list):
    for index, value in enumerate(list):
        if value == 0: continue
        print str(unichr(index + 97)) + ": " + str(value)
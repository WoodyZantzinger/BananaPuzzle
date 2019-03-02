import nltk
from collections import Counter
import copy
import utils
import random

STATIC_BOARD_SIZE = 50
Words_Added = 0

#Makes an empty 150x150 array of "0"
empty_grid = [[0 for x in range(STATIC_BOARD_SIZE)] for y in range(STATIC_BOARD_SIZE)]

#Letter distribution, 0 = # of A's, etc.
MASTER_avail_letters = [13,3,3,6,18,3,4,3,12,2,2,5,3,8,11,3,2,9,6,9,6,3,3,2,3,2]

#ord('a') - 97

#Open a build a corpus of words
f = open('Word_List.txt')
raw = f.read()
tokens = nltk.word_tokenize(raw)
print len(tokens)
tokens.sort(key=len, reverse=True)
print tokens[0]

def findLetterinBoard(board, letter):
    results = []

    for x in range(STATIC_BOARD_SIZE-1):
        for y in range(STATIC_BOARD_SIZE-1):
            if board[x][y] == letter:
                results.append([x,y])

    return results


#Given a board and a set of avail letters, what is the largest word we can place?

def LargestWord (board, avail_letters, words_added) :

    new_board = copy.deepcopy(board)

    #Lets loop through all the words, in largest order
    for current_word in tokens:

        #Skip early words which will suck up our vowels

        if sum(avail_letters) > 40:
            if utils.scoreWord(current_word) < 1.05: continue
        elif sum(avail_letters) > 20:
            if utils.scoreWord(current_word) < 1.25: continue

        #Do we have the letters for it? Store the current state and lets try
        new_avail_letter = copy.deepcopy(avail_letters)

        count = Counter(current_word)
        for letter in count:
            num = ord(letter) - 97
            if new_avail_letter[num] >= count[letter]:
                #we have the letters!
                new_avail_letter[num] = new_avail_letter[num] - count[letter]
            else:
                #we don't so lets reset and try again
                new_avail_letter = copy.deepcopy(avail_letters)
                break

        #if we have the letters, lets check the fit:
        if (new_avail_letter != avail_letters):

            #Is this the first word?
            if (words_added == 0):
                #Place it in the middle and lets move on
                start_x = 15
                start_y = 15
                new_board = copy.deepcopy(board)
                for index, letter in enumerate(current_word):
                    new_board[start_x + index][start_y] = letter

            #most likely not the first word so lets see if there is a spot to put it
            else:
                length = len(current_word)

                #for each letter in the current_word, find potential starting spots and check vertical and horizontal placement

                #Randomize the words so we start in different areas
                shuffled_current_word = list(current_word)
                random.shuffle(shuffled_current_word)

                for letter in shuffled_current_word:
                    locations = findLetterinBoard(board, letter)
                    index = current_word.find(letter)
                    for possible_location in locations:

                        x = possible_location[0]
                        y = possible_location[1]

                        pre_length = index
                        post_length = length - index

                        new_board = copy.deepcopy(board)

                        #Check Vertical
                        for subtract in range(pre_length):
                            if board[x - subtract][y] == 0 or board[x - subtract][y] == current_word[index-subtract]:
                                new_board[x - subtract][y] = current_word[index-subtract]
                            else:
                                #wipe any progress
                                new_board = copy.deepcopy(board)
                                break

                        for add in range(post_length):
                            if board[x + add][y] == 0 or board[x + add][y] == current_word[index + add]:
                                new_board[x + add][y] = current_word[index + add - 1]
                            else:
                                # wipe any progress
                                new_board = copy.deepcopy(board)
                                break

                        #If we couldn't find vertical, we can check horizontal
                        if (new_board == board):

                            for subtract in range(pre_length):
                                if board[x][y - subtract] == 0 or board[x][y - subtract] == current_word[index - subtract]:
                                    new_board[x][y - subtract] = current_word[index - subtract]
                                else:
                                    # wipe any progress
                                    new_board = copy.deepcopy(board)
                                    break

                            for add in range(post_length):
                                if board[x][y + add] == 0 or board[x][y + add] == current_word[index + add]:
                                    new_board[x][y + add] = current_word[index + add]
                                else:
                                    # wipe any progress
                                    new_board = copy.deepcopy(board)
                                    break

                        #Did we write a new board?
                        if (new_board != board): break
                    # Did we write a new board?
                    if (new_board != board): break

        #Were we able to place this word?
        if (new_board != board):
            if sum(new_avail_letter) == 0:
                #we're done! We have full board. Return this board and wrap it up
                return new_board
            else:
                #we have letters left to go, we must go deeper
                words_added += 1
                print "New Word Added!: " + current_word + "\t Letters Remaining: " + str(sum(new_avail_letter))
                if(sum(new_avail_letter) < 10):
                    utils.print_letters(new_avail_letter)
                recursive = LargestWord(new_board, new_avail_letter, words_added)
                if recursive == False:
                    #this path didn't work, we need to try something else
                    new_board = copy.deepcopy(board)
                else:
                    return recursive

    #Did we go through the whole loop without placing a word?
    return False

def main():
    final_board = LargestWord(empty_grid, MASTER_avail_letters, 0)

    for x in final_board:
        for y in final_board:
            print y


if __name__ == "__main__":
    main()


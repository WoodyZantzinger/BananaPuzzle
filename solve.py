import nltk
from collections import Counter
import copy
import utils
import random

WORD_SCORE = 2
FINAL_WORDS = []
BEST_BOARD = None
BEST_BOARD_WORDS = []

# Open a build a corpus of words
f = open('Word_List.txt')
raw = f.read()
tokens = nltk.word_tokenize(raw)
print len(tokens)

#Makes an empty 150x150 array of "0"
empty_grid = [[0 for x in range(utils.STATIC_BOARD_SIZE)] for y in range(utils.STATIC_BOARD_SIZE)]

#Letter distribution, 0 = # of A's, etc.
MASTER_avail_letters = [13,3,3,6,18,3,4,3,12,2,2,5,3,8,11,3,2,9,6,9,6,3,3,2,3,2]

#ord('a') - 97

index_dictionary = {}

last_index = 0

#make an index of where word length are located so we can trim as we go
for index, word in enumerate(tokens):
    if index_dictionary.has_key(len(word)) == False:
        index_dictionary[len(word)] = index
        last_index = index

#Given a board and a set of avail letters, what is the largest word we can place?

def LargestWord (board, avail_letters, words_added, open_spaces) :

    new_board = copy.deepcopy(board)

    #Lets loop through all the words, in largest order

    if sum(avail_letters) == 1: max = last_index
    elif sum(avail_letters) > 25: max = 0
    else: max = index_dictionary[sum(avail_letters)]

    for current_word in tokens[max:]:

        if len(current_word) > sum(avail_letters) + 1: continue

        current_space = None
        skip_index = 0

        #Skip early words which will suck up our vowels
        if sum(avail_letters) > 15:
            if utils.scoreWord(current_word, avail_letters) < WORD_SCORE: continue

        #Do we have the letters for it? Store the current state and lets try
        new_avail_letter = copy.deepcopy(avail_letters)

        for index, letter in enumerate(current_word):
            num = ord(letter) - 97
            if new_avail_letter[num] >= 1:
                #we have the letters!
                new_avail_letter[num] -= 1
                #print "Removed " + letter
            else: #we don't have this letter but can we get it off the board?

                #did we already use an existing tile?
                if current_space != None:
                    new_avail_letter = copy.deepcopy(avail_letters)
                    current_space = None
                    break

                for space in open_spaces:
                    if space[0] == letter:
                        current_space = space
                        skip_index = index
                        break

                if current_space == None:
                    #we searched the letters and open spaces, found nothing
                    new_avail_letter = copy.deepcopy(avail_letters)
                    break

        #we have the letters, but did we find a space? If not, could we still find one? Skip this if this is our first word
        if current_space == None and words_added > 0 and new_avail_letter != avail_letters:
            #for every letter in our word, check all our open spaces for the same letter
            for index, letter in enumerate(current_word):
                for space in open_spaces:
                    if space[0] == letter:

                        #We found an open space!
                        current_space = space
                        #we need to put the tile back!
                        new_avail_letter[ord(letter) - 97] += 1
                        #save our index
                        skip_index = index

                        break
                if current_space != None: break

        #At this point we either found a space or this is the first word or we need to pick a new word
        if (current_space != None or words_added == 0):

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

                #we need to split the word on the chosen letter
                pre_word = current_word[:skip_index]
                post_word = current_word[skip_index + 1:]

                #Do we have the space for it?
                if len(pre_word) < current_space[3] and len(post_word) < current_space[4]:

                    x = current_space[1]
                    y = current_space[2]

                    #Yes, we place the word on the board. Do the "pre" in reverse
                    for index, letter_to_place in enumerate(reversed(pre_word)):
                        if current_space[5] == utils.WORD_VERTICAL:
                            new_board[x - index - 1][y] = letter_to_place
                        else:
                            new_board[x][y - index - 1] = letter_to_place

                    #Yes, we place the word on the board. Do the post
                    for index, letter_to_place in enumerate(post_word):
                        if current_space[5] == utils.WORD_VERTICAL:
                            new_board[x + index + 1][y] = letter_to_place
                        else:
                            new_board[x][y + index + 1] = letter_to_place

        #Were we able to place this word?
        if (new_board != board):
            if sum(new_avail_letter) == 0:
                #we're done! We have full board. Return this board and wrap it up
                FINAL_WORDS.append(current_word)
                return new_board
            else:
                #we have letters left to go, we must go deeper
                words_added += 1


                #if(sum(new_avail_letter) < 15):
                #    utils.print_letters(new_avail_letter)

  #              if (sum(new_avail_letter) < 25):
  #                  for line in new_board: print line
                #print "New Word Added!: " + current_word + "\t Letters Remaining: " + str(sum(new_avail_letter)) + "\t Score:" + str(utils.scoreWord(current_word, avail_letters))
                FINAL_WORDS.append(current_word)
                recursive = LargestWord(new_board, new_avail_letter, words_added, utils.returnBoardOptions(new_board))

                if recursive == False:
                    #this path didn't work, we need to try something else
                    #print "Word Failed: " + current_word
                    new_board = copy.deepcopy(board)
                    words_added -= 1
                    FINAL_WORDS.pop()
                else:
                    return recursive

    #Did we go through the whole loop without placing a word?
    return False

def main():

    try:
        while True:
            # Shuffle, then sort the list by word length

            global FINAL_WORDS
            global BEST_BOARD
            global BEST_BOARD_WORDS

            random.shuffle(tokens)
            tokens.sort(key=len, reverse=True)
            final_board = LargestWord(empty_grid, MASTER_avail_letters, 0, [])

            print "Found a valid board. Words: " + str(len(FINAL_WORDS))

            if len(FINAL_WORDS) < len(BEST_BOARD_WORDS) or BEST_BOARD_WORDS == []:
                #WE FOUND A NEW WINNER!!!
                print "New Best!"
                BEST_BOARD_WORDS = copy.deepcopy(FINAL_WORDS)
                BEST_BOARD = copy.deepcopy(final_board)

            #Wipe everything and go again
            FINAL_WORDS = []


    except KeyboardInterrupt:
        pass
        if BEST_BOARD == None:
            print "We ended before anything was found!"
        else:
            for x in BEST_BOARD:
                row = ""
                for y in x:
                    if y == 0:
                        row = row + " "
                    else:
                        row = row + str(y)
                print row

            print "Final Count: " + str(len(BEST_BOARD_WORDS))
            print "Final Word List: "
            print BEST_BOARD_WORDS




if __name__ == "__main__":
    main()



STATIC_BOARD_SIZE = 50

WORD_HORIZONTAL = -1
WORD_VERTICAL = 1

scrabble_values = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]

def scoreWord(word, letter_bank):
    length = len(word)
    total_score = 0.0

    multiple_score = [a*b for a,b in zip(scrabble_values,letter_bank)]

    for letter in word:
        total_score += scrabble_values[ord(letter) - 97]

    return total_score / length


#Search a board and return every letter which we could build off, its x and y space, its pre and pos space, and its orientation (left, right)
def returnBoardOptions(board):
    results = []
    orient = 0

    for x in range(STATIC_BOARD_SIZE - 1):
        for y in range(STATIC_BOARD_SIZE - 1):
            if board[x][y] != 0:

                #Vertical or Horizontal?
                if board[x+1][y] != 0 or board[x-1][y] != 0:
                    #something is above or below, so this word needs to be laid horizontall
                    orient = WORD_HORIZONTAL
                elif board[x][y+1] != 0 or board[x][y-1] != 0:
                    # something is left or right, so this word needs to be laid vertically
                    orient = WORD_VERTICAL

                pre_space = 0
                post_space = 0

                #Check 30 spaces in both directions (-1 for back, 1 for forward)
                for neg in [-1, 1]:
                    for diff in range(1, 30):
                        new_x = x
                        new_y = y
                        if orient == WORD_VERTICAL: new_x += diff * neg
                        if orient == WORD_HORIZONTAL: new_y += diff * neg

                        #checks if we've gone out of bounds or hit an existing character
                        if (new_x > STATIC_BOARD_SIZE-1 or new_x < 0 or new_y > STATIC_BOARD_SIZE-1 or new_y < 0) or diff == 29 or board[new_x][new_y] != 0:
                            if neg < 0: pre_space = diff - 1
                            if neg > 0: post_space = diff - 1
                            break

                        if orient == WORD_VERTICAL and (board[new_x][new_y + 1] != 0 or board[new_x][new_y - 1] != 0):
                            #There is something above or below this space so it can't be used for a vertical word
                            if neg < 0: pre_space = diff - 1
                            if neg > 0: post_space = diff - 1
                            break

                        if orient == WORD_HORIZONTAL and (board[new_x + 1][new_y] != 0 or board[new_x - 1][new_y] != 0):
                            # There is something left  or right this space so it can't be used for a vertical word
                            if neg < 0: pre_space = diff - 1
                            if neg > 0: post_space = diff - 1
                            break

                #return letter, x pos, y pos, pre space, post space, orientation
                results.append([board[x][y], x, y, pre_space, post_space, orient])
    return results


def findLetterinBoard(board, letter):
    results = []

    for x in range(STATIC_BOARD_SIZE - 1):
        for y in range(STATIC_BOARD_SIZE - 1):
            if board[x][y] == letter:
                results.append([x, y])

    return results


def print_letters(list):
    for index, value in enumerate(list):
        if value == 0: continue
        print str(unichr(index + 97)) + ": " + str(value)
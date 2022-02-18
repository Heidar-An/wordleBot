import pygame as pg
from pygame import *
import random
import math
import json

# defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (115, 165, 90)
TURQUOISE = (64, 224, 208)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
YELLOW = (198, 176, 98)
GREY = (122, 124, 125)

display = [600, 480]
pg.init()
window = pg.display.set_mode(display, pg.RESIZABLE)
smallFont = pg.font.SysFont("Helvetica", 27)
mediumFont = pg.font.SysFont("Helvetica", 50)
window.fill(BLACK)
pg.display.update()

words = []
possibleWords = []
allCommons = {}

wordsGuessedArr = [['#', '#', '#', '#', '#'] for j in range(6)]
inCommonArr = [['B', 'B', 'B', 'B', 'B'] for j in range(6)]
rowNumber = 0


def wordsInit():
    """
    Load in all 5-letter words from the short txt or long txt
    """
    global words
    f = open("shortWords.txt")
    # f = open("words.txt")
    fText = f.read()
    tempString = ""
    for char in fText:
        if char == ',':
            words.append(tempString)
            possibleWords.append(tempString)
            tempString = ""
        elif char != '"':
            tempString += char


def getInCommon():
    """
    Get the key-value pairs for the dictionary for every comparison
    """
    global allCommons
    commonFile = open("data.json", "r")

    pair = commonFile.read().split(",")

    for line in pair:
        line = str(line)
        keyLine, value = line.split()
        keyLine = keyLine[1:len(keyLine) - 2]
        value = value[1: len(value) - 1]
        allCommons[keyLine] = value

    allCommons["cigar:cigar"] = allCommons.pop('"cigar:cigar')


def drawLetters():
    """
    Show the boxes for each letter, and colour it in depending on the comparison
    """
    window.fill(BLACK)

    for j in range(6):
        for i in range(5):
            rect = (0 + 80 * i, 0 + 80 * j, 75, 75)

            colour = GREY
            if wordsGuessedArr[j][i] != '#':
                if inCommonArr[j][i] == 'Y':
                    colour = YELLOW
                elif inCommonArr[j][i] == 'G':
                    colour = GREEN

                text = mediumFont.render(chr(ord(wordsGuessedArr[j][i]) - 32), True, WHITE, colour)

                pg.draw.rect(window, WHITE, rect)
                pg.draw.rect(window, colour, (rect[0] + 2, rect[1] + 2, rect[2] - 4, rect[3] - 4))

                window.blit(text, (rect[0] + 23, rect[1] + 8))
            else:
                pg.draw.rect(window, WHITE, rect)
                pg.draw.rect(window, colour, (rect[0] + 2, rect[1] + 2, rect[2] - 4, rect[3] - 4))

    bestGuesses()
    pg.display.update()


def inCommon(cWord, actualWord):
    """
    Changes the global array for colours in common
    NOT USEFUL DUE TO THE DICTIONARY HAVING THIS PRECOMPUTED
    """
    outputArr = ["B" for i in range(5)]
    letterSeen = [False for i in range(5)]
    global allCommons

    # find green
    for i in range(5):
        if cWord[i] == actualWord[i]:
            outputArr[i] = "G"
            letterSeen[i] = True

    # find yellow
    for indexTwo, char in enumerate(cWord):
        for index, correctChar in enumerate(actualWord):
            if char == correctChar and outputArr[indexTwo] == "B":
                if not letterSeen[index]:
                    letterSeen[index] = True
                    outputArr[indexTwo] = "Y"
                    break
    wordKey = cWord + ":" + actualWord
    value = ""
    for common in outputArr:
        value += common
    allCommons[wordKey] = value


# all possible words  /12,000  instead of 12000 divides by the amount of actual possible words

def everyWord():
    """
    Used to write key-value pairs into json
    """
    file = open("data.json", "w")
    for x in words:
        for y in words:
            inCommon(x, y)
    json.dump(allCommons, file)
    file.close()


def getInformation(word):
    """
    Find how good a particular word is
    """
    global allCommons
    dictionary = {}
    for x in possibleWords:
        commonArr = allCommons[word + ":" + x]
        listCommon = ""
        for value in commonArr:
            listCommon += value
        if listCommon in dictionary:
            dictionary[listCommon] += 1
        else:
            dictionary[listCommon] = 1
    wordSum = 0
    for x in dictionary.values():
        p = x / len(possibleWords)
        wordSum += p * math.log2(1 / p)

    return wordSum


def highestInfo():
    """
    Find the words with the highest entropy
    """
    wordVals = {}
    currentMax = -10000
    currentBestWord = ""

    for x in words:
        information = getInformation(x)

        wordVals[x] = information
        if information > currentMax:
            currentMax = information
            currentBestWord = x

    if len(possibleWords) == 1 or currentMax == 0:
        print("Word with highest entropy: " + possibleWords[0])
        return {"The ": 0, "correct": 0, "word": 0, "is": 0, "definitely": 0, possibleWords[0]: 0}
    else:
        print("Word with highest entropy: " + currentBestWord)
    # return currentBestWord
    return wordVals


def updatePossibleWord(guessWord, colourResult):
    """
    Once a word has been guessed, find all possible remaining words
    """
    for i in range(len(possibleWords) - 1, -1, -1):
        if allCommons[guessWord + ":" + possibleWords[i]] != colourResult:
            possibleWords.pop(i)


def bestGuesses():
    """
    Show the best 6 words
    """
    global wordVals
    # drawLetters()
    wordVals = dict(sorted(wordVals.items(), key=lambda item: item[1], reverse=True))
    text = smallFont.render("E[Info]", True, WHITE)
    window.blit(text, (532, 10))

    text = smallFont.render("Top Picks", True, WHITE)
    window.blit(text, (420, 10))
    for i in range(6):
        text = smallFont.render(str(list(wordVals)[i]), True, WHITE)
        window.blit(text, (420, 50 + 65 * i))

        text = smallFont.render(str(list(wordVals.values())[i]), True, WHITE)
        window.blit(text, (532, 50 + 65 * i))

    pg.display.update()


def init():
    global correctWord, cWord, wordVals, wordsGuessedArr, inCommonArr, rowNumber
    wordsGuessedArr = [['#', '#', '#', '#', '#'] for j in range(6)]
    inCommonArr = [['B', 'B', 'B', 'B', 'B'] for j in range(6)]
    rowNumber = 0
    wordsInit()
    correctWord = random.choice(words)
    print(correctWord)
    cWord = ""
    getInCommon()

    wordVals = highestInfo()
    drawLetters()


init()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if len(cWord) == 5:
                    # arr = inCommon(cWord, correctWord)
                    arr = allCommons[cWord + ":" + correctWord]
                    for index, val in enumerate(arr):
                        inCommonArr[rowNumber][index] = val
                    pg.display.update()
                    updatePossibleWord(cWord, arr)
                    bestGuesses()
                    cWord = ""
                    rowNumber += 1
                    wordVals = highestInfo()

                    # if arr == "GGGGG":
                    #     init()
            elif event.key != pg.K_BACKSPACE and len(cWord) < 5:
                key = event.unicode
                wordsGuessedArr[rowNumber][len(cWord)] = key
                cWord += key
            else:
                cWord = cWord[0: len(cWord) - 1]
                wordsGuessedArr[rowNumber][len(cWord)] = "#"
            drawLetters()

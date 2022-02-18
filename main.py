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

display = [400, 480]
pg.init()
window = pg.display.set_mode(display, pg.RESIZABLE)
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
    global words
    f = open("shortWords.txt")
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

                window.blit(text, (rect[0] + 20, rect[1] + 5))
            else:
                pg.draw.rect(window, WHITE, rect)
                pg.draw.rect(window, colour, (rect[0] + 2, rect[1] + 2, rect[2] - 4, rect[3] - 4))

    pg.display.update()


def inCommon(cWord, actualWord):
    """Changes the global array for colours in common"""
    outputArr = ["B" for i in range(5)]
    letterSeen = [False for i in range(5)]
    global allCommons

    # find green
    for i in range(5):
        if cWord[i] == actualWord[i]:
            outputArr[i] = "G"
            letterSeen[i] = True

    for indexTwo, char in enumerate(cWord):
        for index, correctChar in enumerate(actualWord):
            if char == correctChar and outputArr[indexTwo] == "B":
                if not letterSeen[index]:
                    letterSeen[index] = True
                    outputArr[indexTwo] = "Y"
                    break
    key = cWord + ":" + actualWord
    value = ""
    for common in outputArr:
        value += common
    allCommons[key] = value
    # return outputArr


# guess = hello, 'B' 'B''B' 'B' 'B',

# all possible words  /12,000  instead of 12000 divides by the amount of actual possible words

def everyWord():
    file = open("data.json", "w")
    for index, x in enumerate(words):
        for y in words:
            inCommon(x, y)
    json.dump(allCommons, file)
    file.close()


def getInformation(word):
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
    sum = 0
    for x in dictionary.values():
        p = x / len(possibleWords)
        sum += p * math.log2(1 / p)

    return sum


def highestInfo():
    currentMax = -10000
    currentBestWord = ""

    for x in words:
        information = getInformation(x)

        if information > currentMax:
            currentMax = information
            currentBestWord = x

    if len(possibleWords) == 1 or currentMax == 0:
        return possibleWords[0]

    return currentBestWord


def updatePossibleWord(guessWord, colourResult):
    for i in range(len(possibleWords) - 1, -1, -1):
        if allCommons[guessWord + ":" + possibleWords[i]] != colourResult:
            possibleWords.pop(i)

# (x, y)
drawLetters()
wordsInit()
correctWord = random.choice(words)
print(correctWord)
cWord = ""
getInCommon()

print("Word with highest entropy: " + highestInfo())
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
                    print("Word with highest info: " + highestInfo())
                    cWord = ""
                    rowNumber += 1
            elif event.key != pg.K_BACKSPACE and len(cWord) < 5:
                key = event.unicode
                wordsGuessedArr[rowNumber][len(cWord)] = key
                cWord += key
            else:
                cWord = cWord[0: len(cWord) - 1]
                wordsGuessedArr[rowNumber][len(cWord)] = "#"
            drawLetters()

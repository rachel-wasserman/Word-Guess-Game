# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:08:04 2026

@author: Rachel
"""

import random

def pickRandom():
    words = []
    with open('wordle.txt', 'r') as f:
        for line in f:
            word = ""
            for char in line:
                if char != '\n':
                    word += char
            words.append(word)
    return random.choice(words)


allowedWords = []
with open('wordle-guesses.txt', 'r') as f:
    for line in f:
        word = ""
        for char in line:
            if char != '\n':
                word += char
        allowedWords.append(word)
    
def colorBox(char, status):
    if status == 'G':
        return "\033[42m\033[30m " + char.upper() + " \033[0m"
    elif status == 'Y':
        return "\033[43m\033[30m " + char.upper() + " \033[0m"
    elif status == '_':
        return "\033[100m\033[97m " + char.upper() + " \033[0m"
    else:
        return "\033[97m " + char.upper() + " \033[0m"
    
def colorKey(char, status):
    if status == 'G':
        return "\033[42m\033[30m " + char.upper() + " \033[0m"
    elif status == 'Y':
        return "\033[43m\033[30m " + char.upper() + " \033[0m"
    elif status == 'X':
        return "\033[100m\033[97m " + char.upper() + " \033[0m"
    else:
        return "\033[47m\033[30m " + char.upper() + " \033[0m"

def printBoard(letterBoard, statusBoard):
    for i in range(6):
        printWordle(letterBoard[i], statusBoard[i])  
    
def printWordle(letters, statuses):
    for i in range(5):
        print(colorBox(letters[i], statuses[i]), end="")
    print()
    
def printAlphabet(keyStatus):
    alphabet1 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    alphabet2 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
    alphabet3 = ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    print('Letters Remaining:')
    for char in alphabet1:
        print(colorKey(char, keyStatus[char]), end="")
    print()
    for char in alphabet2:
        print(colorKey(char, keyStatus[char]), end="")
    print()
    for char in alphabet3:
        print(colorKey(char, keyStatus[char]), end="")
    print()
    

def updateKeyStatus(keyStatus, guess, wordle):
    for i in range(5):
        char = guess[i]
        if wordle[i] == 'G':
            keyStatus[char] = 'G'
        elif wordle[i] == 'Y':
            if keyStatus[char] != 'G':
                keyStatus[char] = 'Y'
        elif wordle[i] == '_':
            if keyStatus[char] != 'G' and keyStatus[char] != 'Y':
                keyStatus[char] = 'X'

chosenWord = pickRandom()
print(chosenWord)
print(">>> Welcome to Word Guess Game!")

letterBoard = []
for i in range(6):
    letterBoard.append(['_', '_', '_', '_', '_'])
statusBoard = []
for i in range(6):
    statusBoard.append(['_', '_', '_', '_', '_'])

keyStatus = {}
alphabet = "abcdefghijklmnopqrstuvwxyz"
for char in alphabet:
    keyStatus[char] = 'U'

printBoard(letterBoard, statusBoard)
print()
printAlphabet(keyStatus)

guessed = []
tries = 0
win = False

while tries < 6 and win == False: 
    print()
    guess = input(">>> Guess a word: ").lower()
    
    if guess == chosenWord:
        win = True
        letterBoard[tries] = [guess[0], guess[1], guess[2], guess[3], guess[4]]
        statusBoard[tries] = ['G', 'G', 'G', 'G', 'G']
        updateKeyStatus(keyStatus, guess, statusBoard[tries])
        printBoard(letterBoard, statusBoard)
        print()
        printAlphabet(keyStatus)
    
    elif guess not in allowedWords:
        print("Not a valid word.")
        printBoard(letterBoard, statusBoard)
        print()
        printAlphabet(keyStatus)
    
    elif guess in guessed:
        print("You already guessed that word.")
        printBoard(letterBoard, statusBoard)
        print()
        printAlphabet(keyStatus)
    
    else:
        guessed.append(guess)
        wordle = ['_', '_', '_', '_', '_']
        leftover = []
        
        for i in range(5):
            if guess[i] != chosenWord[i]:
                leftover.append(chosenWord[i])
        for i in range(5):
            if guess[i] == chosenWord[i]:
                wordle[i] = 'G'
        for i in range(5):
            if wordle[i] == '_':
                found = False
                for j in range(len(leftover)):
                    if guess[i] == leftover[j] and found == False:
                        wordle[i] = 'Y'
                        leftover[j] = '*'
                        found = True

        letterBoard[tries] = [guess[0], guess[1], guess[2], guess[3], guess[4]]
        statusBoard[tries] = wordle
        updateKeyStatus(keyStatus, guess, wordle)
             
        printBoard(letterBoard, statusBoard)
        print()
        printAlphabet(keyStatus)
        tries += 1

if not win:
    print()
    print("You lost.")
    print("The correct word was", chosenWord)
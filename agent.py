import random
import re

my_file = open("D:\\AI WORDLE\\cs4811-wordle-main\\resources\\words_alpha.txt", "r")

data = [x for x in my_file.read().split("\n") if len(x) == 5]

secret_word = ""
guess_count = 0

def colorful_print(letter_bank: list):
    for (letter, value) in letter_bank:
        colors: list = [0, 32, 33, 37]
        print(f'\033[0;{colors[value]}m{letter}', end='', sep='', flush=True)
    print('\033[0;37m\n')

def playWordle():
    global secret_word
    global guess_count
    secret_word = random.choice(data)
    guess_count = 0
    print("Welcome to Wordle! You have six guesses to find the word.")
    return

def makeGuess(word):
    global secret_word
    global guess_count
    guess_count += 1
    correct = []
    semi_correct = []
    if guess_count > 6:
        print("No more guesses, Better luck next time")
        return None
    lWord = word.lower()
    if (lWord == secret_word):
        print(f"\033[0;32mCongrats! You guessed the word '{lWord}' in {guess_count} guesses!\033[0;37m")
        return True

    for i in range(0, 5):
        if lWord[i] == secret_word[i]:
            correct.append(i)
            print(f"{lWord[i]} is correct!")
        elif lWord[i] in secret_word:
            semi_correct.append(i)
            print(f"{lWord[i]} is in the wrong position!")

    return (correct, semi_correct)

def giveUp():
    global secret_word
    global guess_count
    guess_count = 6
    print(f"The secret word was {secret_word}. Please try again soon!")
    return

def showState():
    global secret_word
    global guess_count
    print(f"Secret word: {secret_word}. Current guesses used: {guess_count}")
    return

def generate(correct, incorrect):
    token = "".join(incorrect)
    default = f"[^{token}]"
    filled_out = [default if v is None else v for v in correct]
    reg = "".join(filled_out)

    r = re.compile(reg)
    newlist = list(filter(r.match, data))
    return newlist

def play():
    global secret_word
    global guess_count

    correct = [None, None, None, None, None]
    incorrect = []
    almost = []

    playWordle()

    while guess_count < 6:
        if guess_count == 0:
            selected = random.choice(data)
        else:
            selected = random.choice(generate(correct, incorrect))

        print(f"Guessing {selected}")
        out = makeGuess(selected)

        if out == True:
            break
        elif out != None:
            correctOut, almost = out
            for i in range(0, 5):
                if i in correctOut:
                    correct[i] = selected[i]
                elif i in almost:
                    almost.append(selected[i])
                else:
                    incorrect.append(selected[i])

        colorful_print([(l, 1 if l in correct else 2 if l in almost else 3) for l in selected])

    if guess_count >= 6 and secret_word != selected:
        print("\033[0;31mYou Failed, Try Again\033[0;37m")

    showState()

play()


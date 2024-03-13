import requests
import string
import os
from random import choice
from bs4 import BeautifulSoup
from images import images

defined_word: str = ""


# TODO: 1 use the definition to check if the word is in the dictionary, if not then choose another word

def definition(word: str):
    try:
        request = requests.get(f"https://www.merriam-webster.com/dictionary/{word}").text
        soup = BeautifulSoup(request, 'html.parser')
        text = soup.find('span', attrs={'class': 'dtText'}).text
    except AttributeError:
        pass
    else:
        global defined_word
        defined_word = text
        return text


def hint(text: str, guessed: list[str]):
    help_hint = choice(text)
    while help_hint in guessed:
        help_hint = choice(text)
    return help_hint


def clear_screen():
    os.system('cls')


def generate_word():
    try:
        with open("words.txt", mode="r") as file:
            lines = file.read().splitlines()
            line = choice(lines)
    except FileNotFoundError:
        request = requests.get(url="https://www.mit.edu/~ecprice/wordlist.10000")
        words = (request.text.split("\n"))
        with open("words.txt", mode="w") as file:
            for word in words:
                if len(word) > 3:
                    file.write(word + "\n")
    else:
        with open("words.txt", mode="r") as file:
            lines = file.read().splitlines()
            line = choice(lines)
    finally:
        if definition(line):
            return line
        else:
            generate_word()


def win_check(text: str, blanked: list[str]):
    checker = ""
    for _ in blanked:
        checker += _
    if text == checker:
        return True
    else:
        return False


def hang_man():
    global defined_word
    clear_screen()
    game_on = True
    accepted_letters = [x for x in string.ascii_lowercase]
    word = generate_word()
    blanked_word = ['_'] * len(word)
    guessed_letters = []
    lives = 7
    hints = 0
    commands = {
        "Help:": "Show's all available commands",
        "Hint:": "Will let you know a letter in the secret word. You have a maximum of 3 hints",
        "Define:": "Another hint you can use, it will tell you the definition of the secret word 🤫",
        "Exit:": "Exit the game 🥲\n"
    }

    def print_help():
        clear_screen()
        for k, v in commands.items():
            print(k, v)

    while game_on:

        print(images['hangman'][lives])
        print(blanked_word)

        guess = input("Guess a letter: ").lower()

        while guess not in accepted_letters and guess.title() + ":" not in commands.keys():
            guess = input("That's not a letter, try again\nGuess a letter: ").lower()

        if guess == "help":
            print_help()
        elif guess == "exit":
            break
        elif guess == "define":
            clear_screen()
            print(f"Definition{defined_word}")
        elif guess == "hint" and hints < 3:
            clear_screen()
            print(hint(text=word, guessed=guessed_letters))
            hints += 1
        elif guess == "hint" and hints >= 3:
            clear_screen()
            print("You've ran out of hints!")

        if guess in guessed_letters:
            clear_screen()
            print(f"You've already tried the letter: {guess}\nGuess again")
        elif guess in word:
            clear_screen()
            for count, i in enumerate(iterable=word, start=0):
                if i == guess:
                    blanked_word[count] = guess
            guessed_letters.append(guess)
        elif guess.title() + ":" not in commands.keys():
            clear_screen()
            lives -= 1
            print(f"Too bad, you have {lives} guesses left")
            guessed_letters.append(guess)

        if win_check(word, blanked_word):
            print(images["win"])
            print(f"Congratulations, you win!\nThe word was: {word}")
            game_on = False

        if lives == 0:
            print(images["lose"])
            print(f"Sorry, you loose, the word was: {word}")
            game_on = False

    play_again = input("Would you like to play again? (Y/N): ").upper()
    if play_again == "Y":
        clear_screen()
        hang_man()
    else:
        clear_screen()
        print("Thanks for playing, see you soon 😵")


play = input("Would you like to play hangman (Y/N): ").upper()
clear_screen()
print(images["title"])
print("Welcome to Hangman, it's time to guess the word, you can type 'help' to show a list of commands")
input("Press any key to continue: ")
hang_man()

if play == "Y":
    hang_man()

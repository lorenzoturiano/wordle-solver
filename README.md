## Wordle

Wordle is a word-guessing game, where you have 6 attempts to guess a 5-letter word.
You can play it here: https://www.nytimes.com/games/wordle/index.html

With each guess, you learn whether you correctly guessed a character (and its position), whether a character appears in the word but in a different position, or does not appear in the word at all.


## Project

The Wordle program contains three classes:
- `game.py` runs n games of Wordle coordinating the other two classes and keeps track of the scores. This script creates a new guesser object for every run.
- `wordle.py` implements the game of Wordle, from choosing the word to guess to checking the correctness of a guess.
- `guesser.py` produces a guess word.

You also have two wordlists in tsv and yaml format:
1. `train_wordlist` (named as `wordlist` in the folder) contains ca. 4k words along with their frequency in an unnamed corpus, to be used for training. Using the word frequency data (e.g. to compute character n-gram probabilities) is completely optional.
2. `dev_wordlist` contains another 500 words for development, matching the size of the test set.

## How to run

How to run n games of Wordle

If YOU want to play one round:
`python game.py --r n`. <br>

If you want the SCRIPT to play n rounds:
`python game.py --r n --p`. <br>

When you run this command, the program will output some stats about the success rate.


### 🏅 Assessment

We will evaluate your `guesser.py` on a secret test set containing 500 words.
Your grade will be based on a combination of:
1. How often your `guesser.py` correctly guesses the word.
2. The average number of tries it takes to produce a correct guess.
3. The time it takes to produce 500 guesses on the test set.


- Your guess can be any 5-letter string.
It does not have to be a word.
However, the solution will always be drawn from the wordlist (which contains only words).

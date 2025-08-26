from random import choice
import yaml
from rich.console import Console
import math
from collections import defaultdict, Counter

class Guesser:
    '''
        INSTRUCTIONS: This function should return your next guess. 
        Currently it picks a random word from wordlist and returns that.
        You will need to parse the output from Wordle:
        - If your guess contains that character in a different position, Wordle will return a '-' in that position.
        - If your guess does not contain thta character at all, Wordle will return a '+' in that position.
        - If you guesses the character placement correctly, Wordle will return the character. 

        You CANNOT just get the word from the Wordle class, obviously :)
    '''
    def __init__(self, manual):
        self.word_list = yaml.load(open('dev_wordlist.yaml'), Loader=yaml.FullLoader)
        self.og_word_list = self.word_list
        self._manual = manual
        self.console = Console()
        self._tried = []
        self.result_cache = {}
        self.entropy_cache = {}

    def restart_game(self):
        self._tried = []
        self.word_list = self.og_word_list

    def get_result(self, guess, word):
        key = (guess, word)
        if key in self.result_cache:
            return self.result_cache[key]

        counts = Counter(word)
        results = ['+' for _ in guess]

        for i, letter in enumerate(guess):
            if guess[i] == word[i]:
                results[i] = guess[i]
                counts[guess[i]] -= 1

        for i, letter in enumerate(guess):
            if guess[i] != word[i] and counts.get(guess[i], 0) > 0:
                results[i] = '-'
                counts[guess[i]] -= 1

        result_str = ''.join(results)
        self.result_cache[key] = result_str
        return result_str

    def compute_entropy(self, guess):
        """
        Compute the entropy for a given guess based on the provided word_list.
        Uses caching to avoid recomputation if the guess and word_list state is unchanged.
        """
        key = (guess, tuple(self.word_list))
        if key in self.entropy_cache:
            return self.entropy_cache[key]

        total_words = len(self.word_list)
        pattern_counts = defaultdict(int)

        for target in self.word_list:
            if guess != target:
                result = self.get_result(guess, target)
                pattern_counts[result] += 1

        probabilities = [count / total_words for count in pattern_counts.values()]
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)

        self.entropy_cache[key] = entropy
        return entropy
    
    def get_best_guess(self):
        """
        Finds the word with highest entropy to use as the next guess.
        
        Returns:
            str: Word with highest entropy or random word if list is empty/single word
        """ 
        if len(self.word_list) == 1:
            return self.word_list[0]
            
        best_guess = None
        max_entropy = float('-inf')
        
        for word in self.word_list:
            entropy = self.compute_entropy(word)
            if entropy > max_entropy:
                max_entropy = entropy
                best_guess = word
                
        return best_guess

    def update_word_list(self, guess, result):
        """
        Updates the list of possible words based on Wordle feedback.
        
        Args:
            guess (str): The guessed word
            result (str): Feedback string where:
                - lowercase = green (correct position)
                - '-' = yellow (wrong position)
                - '+' = grey (not in word)
            word_list (list): Current list of possible words
            
        Returns:
            list: Updated list of possible words matching the feedback
        """
        letter_count_in_result = {}
        for i, res in enumerate(result):
            if res.islower() or res == '-':
                letter_count_in_result[guess[i]] = letter_count_in_result.get(guess[i], 0) + 1
        
        new_word_list = []
        green_positions = {i: guess[i] for i, res in enumerate(result) if res.islower()}
        yellow_letters = {i: guess[i] for i, res in enumerate(result) if res == '-'}
        
        for word in self.word_list:
            if word == guess:
                continue
                
            if any(word[pos] != letter for pos, letter in green_positions.items()):
                continue
                
            valid = True
            must_contain = {}
            
            for pos, letter in yellow_letters.items():
                if letter not in word:
                    valid = False
                    break
                if word[pos] == letter:
                    valid = False
                    break
                must_contain[letter] = must_contain.get(letter, 0) + 1
            
            if not valid:
                continue
                
            for i, res in enumerate(result):
                if res == '+':
                    letter = guess[i]
                    if letter in letter_count_in_result:
                        if word.count(letter) != letter_count_in_result[letter]:
                            valid = False
                            break
                    elif letter in word:
                        valid = False
                        break
            
            if valid and all(word.count(letter) >= count for letter, count in must_contain.items()):
                new_word_list.append(word)
        
        return new_word_list

    def get_guess(self, result):
        '''
        This function must return your guess as a string.
        
        '''
        if self._manual=='manual':
            return self.console.input('Your guess:\n')
        else:
            if self._tried:
                last_guess = self._tried[-1]
                self.word_list = self.update_word_list(last_guess, result)
        
            if self._tried:
                guess = self.get_best_guess()
            else:
                guess ='salet'
            self._tried.append(guess)
            self.console.print(guess)
            return guess
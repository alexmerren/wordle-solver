import sys
import re
import flag

class Flags():
    """
    Class to store the flag values provided by the flag package

    Attributes:
        used (string): A string of characters
        correct (string): A string of characters
        placement (string): A string of character and number pairs
    """
    used = flag.string("used", "", "The letters that are grey-ed out.")
    correct = flag.string("correct", "", "The letters that are highlighted in yellow.")
    placement = flag.string("placement", "", "The letters that are highlighted in green, along with their position: 'A' in position 1 would be \"a1\".")

    def __init__(self):
        flag.parse()

class Solver():
    """
    Class to encapsulate methods to narrow down the possible words

    Args:
        flag_values (Flags): The values parsed by the flag package

    Attributes:
        used (string): A string of characters
        correct (string): A string of characters
        placement (string): A string of character and number pairs
        words (list): A list of valid scrabble words
    """
    filename = "words.txt"
    wordsize = 5

    def __init__(self, flag_values):
        self.used = flag_values.used
        self.correct = flag_values.correct
        self.placement = flag_values.placement
        self.words = self.load_word_list()

    def load_word_list(self):
        """ Load words from a file to use to narrow down the answer to wordle """
        words = []
        with open(self.filename) as file:
            for line in file:
                if len(line) == self.wordsize + 1:
                    words.append(line.rstrip())
        return words

    def build_expression_must_contain_one(self, used_string):
        """
        Build a regular expression that matches if there is at least one character present

        Args:
            used_string (string): A string of characters

        Returns:
            A string containing a regular expression
        """
        expression = f'[{set(used_string.upper())}]'
        return expression

    def build_expression_must_contain_all(self, correct_string):
        """
        Build a regular expression that matches if all characters are present

        Args:
            correct_string (string): A string of characters

        Returns:
            A string containing a regular expression
        """
        expression = ""
        for letter in set(correct_string.upper()):
            expression += f'(?=\\w*{letter})'
        expression += "\\w+"
        return expression

    def check_placement_is_correct(self, placement_string, word):
        """
        Check that placement that is specified is correct in a given word

        Args:
            placement_string (str): A string of character and number pairs
            word (str): A word to check the placement of letters of

        Returns:
            A boolean that is True if the placement matches, and False is the
            given placement_string does not match.
        """
        if len(placement_string) == 0 :
            return True

        for index in range(0, len(placement_string), 2):
            letter_in_word = word[int(placement_string[index + 1]) - 1]
            letter_in_string = placement_string[index].upper()
            if letter_in_word != letter_in_string:
                return False

        return True

    def find_possible_words(self):
        """
        Run given searches on a word to check if it is valid

        Returns:
            A list of words that match all the cases presented by the
            regular expressions, and placement string.

        """
        final_words = []
        used_expression = self.build_expression_must_contain_one(self.used)
        correct_expression = self.build_expression_must_contain_all(self.correct)
        for word in self.words:
            if (
                not re.search(used_expression, word)
                and re.search(correct_expression, word)
                and self.check_placement_is_correct(self.placement, word)
            ):
                final_words.append(word)

        return final_words

def main():
    """
    solver.py goes through the valid scrabble words and reduces the amount of
    valid words given some parameters, these parameters are given by the output
    of the wordle game.
    """
    values = Flags()
    solver = Solver(values)
    possible_words = solver.find_possible_words()
    print(possible_words)

if __name__ == "__main__":
    main()

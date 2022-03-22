import os
import re
import flag

ALL_WORDS_FILE = os.path.abspath("all_words.txt")
FIVE_LETTER_WORDS_FILE = os.path.abspath("five_letter_words.txt")
WORD_SIZE = 6  

def define_flags():
    grey = flag.string("grey", "", "The letters that are grey-ed out.")
    yellow = flag.string("yellow", "", "The letters that are highlighted in yellow, along with their position: 'C' in position 5 would be \"c5\".")
    green = flag.string("green", "", "The letters that are highlighted in green, along with their position: 'A' in position 1 would be \"a1\".")
    return grey, yellow, green

def load_all_words_for_length(filename):
    words = []
    with open(filename) as words_file:
        [words.append(line.rstrip()) for line in words_file if len(line) == WORD_SIZE]
    return words

def load_words(filename):
    words = []
    with open(filename) as words_file:
        [words.append(line.rstrip()) for line in words_file]
    return words

def build_expression_must_contain_one(grey_string):
    expression = f'[{set(grey_string.upper())}]'
    return expression

def build_expression_must_contain_all(yellow_string):
    expression = ""
    for element in yellow_string[::2]:
        expression += f'(?=\\w*{element.upper()})'
    expression += "\\w+"
    return expression

def check_yellow_placement(yellow_string, word):
    if len(yellow_string) == 0:
        return True

    for index in range(0, len(yellow_string), 2):
        letter_in_word = word[int(yellow_string[index + 1]) - 1]
        letter_in_string = yellow_string[index].upper()
        if letter_in_word == letter_in_string:
            return False

    return True

def check_green_placement(green_string, word):
    if len(green_string) == 0:
        return True

    for index in range(0, len(green_string), 2):
        letter_in_word = word[int(green_string[index + 1]) - 1]
        letter_in_string = green_string[index].upper()
        if letter_in_word != letter_in_string:
            return False

    return True

def filter_words(words, grey_string, yellow_string, green_string):
    filtered_words = []
    grey_expression = build_expression_must_contain_one(grey_string)
    yellow_expression = build_expression_must_contain_all(yellow_string)
    for word in words:
        if (
            not re.search(grey_expression, word) and re.search(yellow_expression, word)
            and check_yellow_placement(yellow_string, word) and check_green_placement(green_string, word)
        ):
            filtered_words.append(word)

    return filtered_words

def main():
    grey, yellow, green = define_flags()
    flag.parse()
    words = load_words(FIVE_LETTER_WORDS_FILE)
    final_words = filter_words(words, grey, yellow, green)
    print(final_words)

if __name__ == "__main__":
    main()


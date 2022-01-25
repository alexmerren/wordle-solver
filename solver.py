import sys
import re
import flag

class Flags():
    def __init__(self):
        self.used = flag.string("used", "", "The letters that are grey-ed out.")
        self.correct = flag.string("correct", "", "The letters that are highlighted in yellow.")
        self.placement = flag.string("placement", "", "The letters that are highlighted in green, along with their position: 'A' in position 1 would be \"a1\".")
        flag.parse()

class WordleBot():
    filename = "words.txt"
    wordsize = 5

    def __init__(self, flagValues):
        self.used = flagValues.used 
        self.correct = flagValues.correct 
        self.placement = flagValues.placement
        self.words = self.loadWordList()

    def loadWordList(self):
        words = []
        with open(self.filename) as file:
            for line in file:
                if len(line) == self.wordsize + 1:
                    words.append(line.rstrip())
        return words

    def buildExpression_MustContainOne(self, usedString):
        expression = f'[{set(usedString.upper())}]'
        return expression 

    def buildExpression_MustContainAll(self, correctString):
        expression = ""
        for letter in set(correctString.upper()):
            expression += f'(?=\\w*{letter})'
        expression += "\\w+"
        return expression 

    def checkPlacementIsCorrect(self, placementString, word):
        if len(placementString) == 0 :
            return True 

        for index in range(0, len(placementString), 2): 
            letterInWord = word[int(placementString[index + 1]) - 1]
            letterInString = placementString[index].upper()
            if letterInWord != letterInString:
                return False

        return True 

    def FindPossibleWords(self):
        finalWords = []
        usedExpression = self.buildExpression_MustContainOne(self.used)
        correctExpression = self.buildExpression_MustContainAll(self.correct)
        for word in self.words:
            if ( 
                not re.search(usedExpression, word)
                and re.search(correctExpression, word)
                and self.checkPlacementIsCorrect(self.placement, word)
            ):
                finalWords.append(word)

        return finalWords

def main():
    values = Flags()
    bot = WordleBot(values)
    possibleWords = bot.FindPossibleWords()
    print(possibleWords)

if __name__ == "__main__":
    main()

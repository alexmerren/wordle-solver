# Wordle Solver

This is just a simple wordle bot that can be used to get the correct answer to any wordle.

## Installation

Clone the repo, install Python3 and you're done! (basically).

## Usage

In order to use the program, it uses the [Flag](https://pypi.org/project/Flag/) package of Python.

The program should complain if the flags are not used correctly, but if not, here is the usage:

```
usage: bot.py [-h] [--used USED] [--correct CORRECT] [--placement PLACEMENT]

optional arguments:
  -h, --help            show this help message and exit
  --used USED           The letters that are grey-ed out.
  --correct CORRECT     The letters that are highlighted in yellow.
  --placement PLACEMENT
                        The letters that are highlighted in green, along with their position: 'A' in position 1 would be "a1". 
```

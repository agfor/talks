#!/usr/bin/env python3

import sys
assert sys.version[0] == '3'

from random import choice
from itertools import product
from collections import Counter, defaultdict

from iteratedgame import IteratedGame

class Settings:
    def __init__(self, *,
                 colors = '123456',
                 correct = 'B',
                 near = 'W',
                 wrong = '.',
                 pegs = 4,
                 max_guesses = 10,
                 _all_answers = None):
        for setting, value in locals().items():
            setattr(self, setting, value)

        self.victory = correct * pegs
        self.default_score = wrong * pegs

    def random_answer(self):
        return "".join(choice(self.colors) for _ in range(self.pegs))

    @property
    def all_answers(self):
        if not self._all_answers:
            self._all_answers = set("".join(answer) for answer in product(self.colors, repeat = self.pegs))
        return self._all_answers

class Mastermind(IteratedGame):
    DEFAULT_SETTINGS = Settings()

    def calculate_score(self, guess, answer = None):
        if answer == None:
            answer = self.answer

        score = []
        wrong_guess_pegs = []
        wrong_answer_pegs = []

        for guess_peg, answer_peg in zip(guess, answer):
            if guess_peg == answer_peg:
                score.append(self.settings.correct)
            else:
                wrong_guess_pegs.append(guess_peg)
                wrong_answer_pegs.append(answer_peg)

        for peg in wrong_guess_pegs:
            if peg in wrong_answer_pegs:
                wrong_answer_pegs.remove(peg)
                score.append(self.settings.near)

        return "".join(score) + self.settings.default_score[len(score):]

    def guess_valid(self, guess):
        return len(guess) == self.settings.pegs and all(letter in self.settings.colors for letter in guess)

class InteractiveMastermind(Mastermind):
    def guesser(self):
        print("Guesses Remaining:", self.guesses_left)
        while not (yield input("Guess: ")):
            print("Score:", self.score)
            print("Guesses Remaining:", self.guesses_left)

        if self.won:
            print("Correct! It took you", self.guesses, "guesses.")
        else:
            print("Sorry! The correct answer was", self.answer)
        yield

class AutoMastermind(Mastermind):
    def answer_matches(self, answer, guess, score):
        return self.calculate_score(guess, answer) == score

    def matching_answers(self, guess, score, answers):
        return {answer for answer in answers if self.answer_matches(answer, guess, score)}

    def guesser(self):
        working_set = all_answers = self.settings.all_answers
        guess = "1122"
        print(guess)

        while not (yield guess):
            print(self.score)
            working_set = self.matching_answers(guess, self.score, working_set)
            answers, guess = min((len(self.matching_answers(answer, self.score, working_set)), answer)
                                 for answer in working_set)
            print(guess, ":", answers)

        print(self.guesses if self.won else self.answer)
        yield

class KnuthMastermind(AutoMastermind):
    def __init__(self, *args, _tables = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._tables = _tables or defaultdict(dict)

    @property
    def tables(self):
        if not self._tables:
            for guess, answer in product(self.settings.all_answers, repeat = 2):
                guess = "".join(guess)
                answer = "".join(answer)
                self._tables[guess][answer] = self.calculate_score(guess, answer)
        return self._tables


    def guesser(self):
        tables = self.tables.copy()
        working_set = self.settings.all_answers
        guess = "1122"
        print(guess, ":", True, ":", len(working_set))

        while not(yield guess):
            print(self.score)
            working_set = self.matching_answers(guess, self.score, working_set)
            guesses = []
            for answer, table in tables.items():
                tables[answer] = table = {key: value for key, value in table.items() if key in working_set}
                guesses.append((max(Counter(table.values()).values()), answer not in working_set, answer))

            answers, not_in_working_set, guess = min(guesses)
            print(guess, ":", not not_in_working_set, ":", len(working_set))

        print(self.guesses if self.won else self.answer)
        yield

if __name__ == "__main__":
    game = InteractiveMastermind()
    # game = KnuthMastermind()
    # while True:
    #     game.play()

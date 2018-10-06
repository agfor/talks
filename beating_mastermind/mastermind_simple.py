#!/usr/bin/env python3

import collections
import functools
import itertools
import random
import sys

assert sys.version[0] == '3'

class Mastermind:
    def __init__(self):
        self.all_answers = set(itertools.product("123456", repeat = 4))
        self.all_scores = collections.defaultdict(dict)

        for guess, answer in itertools.product(self.all_answers, repeat = 2):
            self.all_scores[guess][answer] = self.calculate_score(guess, answer)

    def play(self):
        self.guesses = 0
        self.answer = tuple(random.choice("123456") for _ in range(4))
        self.possible_scores = self.all_scores.copy()
        self.possible_answers = self.all_answers

        while self.guesses < 10:
            self.guess = self.make_guess()
            if self.guess in self.all_answers:
                self.guesses += 1
                self.score = self.calculate_score(self.guess, self.answer)
                if self.score == ("B",) * 4:
                    print(self.guesses, "".join(self.guess))
                    break

    def calculate_score(self, guess, answer):
        score = []
        wrong_guess_pegs = []
        wrong_answer_pegs = []

        for guess_peg, answer_peg in zip(guess, answer):
            if guess_peg == answer_peg:
                score.append("B")
            else:
                wrong_guess_pegs.append(guess_peg)
                wrong_answer_pegs.append(answer_peg)

        for peg in wrong_guess_pegs:
            if peg in wrong_answer_pegs:
                wrong_answer_pegs.remove(peg)
                score.append("W")

        return tuple(score)

    def make_guess(self):
        if self.guesses:
            self.possible_answers = {answer for answer in self.possible_answers
                    if self.all_scores[self.guess][answer] == self.score}
            guesses = []

            for guess, scores_by_answer in self.possible_scores.items():
                scores_by_answer = {answer: score for answer, score
                        in scores_by_answer.items() if answer in self.possible_answers}
                self.possible_scores[guess] = scores_by_answer
                possibilities_per_score = collections.Counter(scores_by_answer.values())
                worst_case_possibilities = max(possibilities_per_score.values())
                guess_is_impossible = guess not in self.possible_answers
                guesses.append((worst_case_possibilities, guess_is_impossible, guess))

            return min(guesses)[-1]
        else:
            return ("1", "1", "2", "2")

if __name__ == "__main__":
    game = Mastermind()
    while True:
        game.play()

class IteratedGame:
    def __init__(self, settings = None):
        if settings is None:
            self.settings = self.DEFAULT_SETTINGS
        else:
            self.settings = settings

    def reset(self, answer = None):
        self.guesses = 0
        self.score = self.settings.default_score
        self.answer = answer or self.settings.random_answer()

    @property
    def guesses_left(self):
        return self.settings.max_guesses - self.guesses

    @property
    def won(self):
        return self.score == self.settings.victory

    def guess(self, guess):
        if self.guesses_left and self.guess_valid(guess):
            self.guesses += 1;
            self.score = self.calculate_score(guess)

    def play(self, answer = None):
        self.reset(answer)
        guesser = self.guesser()
        while self.guesses_left and not self.won:
            self.guess(next(guesser))

        guesser.send(True)
        return self.guesses

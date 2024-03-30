import random

# Global mistake_chance parameter
mistake_chance = 0.05


class Bot():
    def __init__(self):
        self.history = []

    def move(self):
        raise NotImplementedError

    def append_history(self, move):
        self.history.append(move)


class AlwaysCooperate(Bot):
    def __init__(self):
        super().__init__()

    def move(self):
        return "C"


class AlwaysBetray(Bot):
    def __init__(self):
        super().__init__()

    def move(self):
        return "N"


class Copycat(Bot):
    def __init__(self):
        super().__init__()

    def move(self):
        if len(self.history) < 1:
            return "C"
        return self.history[-1]


class Copykitten(Bot):
    def __init__(self):
        super().__init__()
        self.retaliating = False
        self.cheat_count = 0

    def move(self):
        global mistake_chance
        if len(self.history) == 0:
            return "C"

        if random.random() < mistake_chance:
            return "N" if self.history[-1] == "C" else "C"

        if not self.retaliating:
            if self.history[-1] == "N":
                self.cheat_count += 1
            else:
                self.cheat_count = 0
            if self.cheat_count >= 2:
                self.retaliating = True
            return self.history[-1]
        else:
            return "N"


class Simpleton(Bot):
    def __init__(self):
        super().__init__()
        self.last_move = "C"

    def move(self):
        global mistake_chance
        if len(self.history) == 0:
            return "C"

        if random.random() < mistake_chance:
            return "N" if self.last_move == "C" else "C"

        if self.history[-1] == "C":
            return self.last_move
        else:
            self.last_move = "C" if self.last_move == "N" else "N"
            return self.last_move


class Random(Bot):
    def __init__(self):
        super().__init__()

    def move(self):
        global mistake_chance
        if random.random() < mistake_chance:
            return random.choice(["C", "N"])
        return random.choice(["C", "N"])


class Grudger(Bot):
    def __init__(self):
        super().__init__()
        self.betrayed = False

    def move(self):
        if self.betrayed:
            return "N"
        elif len(self.history) > 0 and self.history[-1] == "N":
            self.betrayed = True
            return "N"
        else:
            return "C"


class Detective(Bot):
    def __init__(self):
        super().__init__()
        self.pattern = ["C", "N", "C", "C"]
        self.retaliate = False

    def move(self):
        if len(self.history) < len(self.pattern):
            return self.pattern[len(self.history)]
        elif "N" in self.history:
            self.retaliate = True
        if self.retaliate:
            if len(self.history) < 2:
                return "C"
            return self.history[-1]
        else:
            return "N"

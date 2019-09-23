class AlterBot:
    def __init__(self):
        self.counter = 1
        self.dyno = 100

    def make_move(self, gamestate):
        if self.counter == 1:
            self.counter = 2
            return 'W'
        elif self.dyno != 0:
            self.counter = 1
            self.dyno -= 1
            return 'D'
        else:
            return 'W'

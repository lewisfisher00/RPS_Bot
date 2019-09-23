class MyBot:
    def __init__(self):
        self.my_dynamite = 100
        self.opp_dynamite = 100
        self.previous_moves = {'R': 0, 'P': 0, 'S': 0, 'D': 0, 'W': 0}
        self.round = 0

    def get_valid_moves(self):
        if self.opp_dynamite == 0:
            if self.my_dynamite == 0:
                return ['P', 'S', 'R']
            return ['P', 'R', 'S', 'D']
        else:
            if self.my_dynamite == 0:
                return ['P', 'S', 'R', 'W']
            return ['P', 'R', 'S', 'D', 'W']

    def make_move(self, gamestate):
        if self.get_last_move(gamestate) == 'D':
            self.opp_dynamite -= 1
        available_moves = self.get_valid_moves()
        if self.round < 5:
            move = self.random_move(available_moves, gamestate)
        else:
            self.previous_moves[self.get_last_move(gamestate)] += 1
            most_common = self.find_most_used()
            move = self.counter_most_common(most_common, gamestate)
        if move == 'D':
            self.my_dynamite -= 1
        self.round += 1
        return move

    def counter_most_common(self, most_common, gamestate):
        counter = {'R': lambda: 'P', 'P': lambda: 'S', 'S': lambda: 'R', 'D': lambda: 'W',
                   'W': lambda: self.random_move(['R', 'P', 'S'], gamestate)}
        choice = counter[most_common]()
        round_point = self.round_point(gamestate)
        if choice != 'W':
            move_options = [choice, choice, 'D']
            for _ in range(round_point - 1):
                move_options.append('D')
            choice = self.decide_if_dynamite(gamestate, move_options)
        return choice

    def round_point(self, gamestate):
        check_round = self.round - 1
        round_point = 1
        while check_round >= 0:
            if gamestate["rounds"][check_round]["p1"] == gamestate["rounds"][check_round]["p2"]:
                round_point += 1
                check_round -= 1
            else:
                return round_point

    def decide_if_dynamite(self, gamestate, choices):
        if self.my_dynamite == 0:
            return self.random_move(['R', 'P', 'S'], gamestate)
        choice = self.random_move(choices, gamestate)
        return choice

    def find_most_used(self):
        most_common = ''
        most_amount = -1
        for move in self.previous_moves:
            if self.previous_moves[move] > most_amount:
                most_common = move
                most_amount = self.previous_moves[move]
        move_to_make = most_common
        self.previous_moves[most_common] = int(self.previous_moves[most_common]*(7/8))
        return move_to_make

    def random_move(self, available_moves, gamestate):
        return available_moves[abs(hash(str(gamestate) + str(self))) % len(available_moves)]

    def get_last_move(self, gamestate):
        if len(gamestate["rounds"]) == 0:
            return None
        last_move = gamestate["rounds"][-1]["p2"]
        return last_move

import random
import sys
from read import readInput
from write import writeOutput


class RandomPlayer():
    def __init__(self):
        self.type = 'random'

    def get_input(self, go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):
                    possible_placements.append((i,j))
        if not possible_placements:
            return "PASS"
        else:
            action = random.choice(possible_placements)
            x,y = action
            writeOutput(action)
            return action

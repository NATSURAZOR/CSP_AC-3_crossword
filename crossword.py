############################### CLASS DEFINITION ##############################
import numpy as np


class Word:
    def __init__(self, row, col, l, d):
        self.row = row
        self.col = col
        self.l = l
        self.d = d
        self.value = None

    def __len__(self):
        return self.l

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.d == other.d

    def __repr__(self):
        return f'Word({self.row}, {self.col}, {self.l}, {self.d}, {self.value})'

class Connection:
    def __init__(self, word1, word2, row, col):
        self.word1 = word1
        self.word2 = word2 
        self.row = row
        self.col = col

    def __repr__(self):
        return f'Connection({self.word1}, {self.word2}, {self.row}, {self.col})'

class CrossWord():
    # Dict of possible directions {name: (delta_row, delta_col)}
    directions = {'down': (1, 0), 'right': (0, 1)}

    def __init__(self, grid, words):
        self.grid = grid
        self.positions = [Word(*w) for w in self.get_positions(grid)]
        self.connections = []
        self.words = words
        self.domains = list()
        self.set_domains()
        self.perform_node_consistency()
        print(self.connections)
        # self.arc_consistency = self.set_arc_consistency()


    def get_positions(self, grid):
        # Computes list of all possible positions for words.
        # Each position is a touple: (start_row, start_col, length, direction),
        # and length must be at least 2, i.e. positions for a single letter
        # (length==1) are omitted.
        # Note: Currently only for 'down' and 'right' directions.
        def check_line(line):
            res = []
            start_i, was_space = 0, False
            for i in range(len(line)):
                if line[i] == '#' and was_space:
                    was_space = False
                    if i - start_i > 1:
                        res.append((start_i, i - start_i))
                elif line[i] == ' ' and not was_space:
                    start_i = i
                    was_space = True
            return res

        poss = []
        for r in range(len(grid)):
            row = grid[r]
            poss = poss + [(r, p[0], p[1], 'right') for p in check_line(row)]
        for c in range(len(grid[0])):
            column = [row[c] for row in grid]
            poss = poss + [(p[0], c, p[1], 'down') for p in check_line(column)]
        return poss

    def print_grid(self):
        # Pretty prints the crossword
        for row in self.grid:
            print(''.join(row))

    def text_at_pos(self, position):
        # Returns text actually written in specified position.
        dr, dc = self.directions[position[3]]
        r, c = position[0], position[1]
        return ''.join([self.grid[r + i * dr][c + i * dc] for i in range(position[2])])

    def write_word(self, position, word):
        # Writes word to specified position and direction.
        # Note: this method does not check whether the word can be placed into
        # specified position.
        dr, dc = self.directions[position[3]]
        r, c = position[0], position[1]
        for i in range(position[2]):
            self.grid[r + i * dr][c + i * dc] = word[i]

    def can_write_word(self, position, word):
        # Check whether the word can be placed into specified position,
        # i.e. position is empty, or all letters within the position are same
        # as those in the word.
        ### YOUR CODE GOES HERE ###
        pass

    # ----
    def set_arc_consistency(self):
        def create_points_right(pos, number):
            array_pos[number] = {(pos[0], pos[1] + increment) for increment in range(pos[2])}

        def create_points_down(pos, number):
            array_pos[number] = {(pos[0] + increment, pos[1]) for increment in range(pos[2])}

        def set_array_of_word_position():
            [create_points_right(pos, number)
             if pos[3] == "right"
             else create_points_down(pos, number)
             for number, pos in enumerate(self.positions)]

        def have_same_point():
            related_pos = []
            for pos1 in array_pos:
                for pos2 in array_pos:
                    if pos1 != pos2:
                        if bool(array_pos[pos1] & array_pos[pos2]):
                            related_pos.append((self.positions[pos1], self.positions[pos2]))
            return related_pos

        array_pos = []
        set_array_of_word_position()
        print(array_pos)
        return have_same_point()

    # ----------- create domains --------------------------------------------------------------------------------------------
    def set_domains(self):
        [self.set_words_to_domain(domain_number, len(self.positions[domain_number]))
         for domain_number in range(len(self.positions))]

    def set_words_to_domain(self, domain_id, word_length):
        self.domains.append([])
        [self.domains[domain_id].append(word) for word in self.words if len(word) == word_length]


    #------------ node consistency ------------------------------------------------------------------------------------------
    def perform_node_consistency(self):
        self.find_connections()
        # TODO

    def find_connections(self):
        for i in range(len(self.positions)):
            for j in range(i+1, len(self.positions)):
                word1 = self.positions[i]
                word2 = self.positions[j]
                if word1.d != word2.d:
                    if word1.d == 'right' and word2.row <= word1.row and word2.row + len(word2) >= word1.row:
                        if word2.col >= word1.col and word1.col + len(word1) >= word2.col:
                            self.connections.append(Connection(word1, word2, word1.row, word2.col))
                    elif word1.d == 'down' and word2.col <= word1.col and word2.col + len(word2) >= word1.col:
                        if word2.row >= word1.row and word1.row + len(word1) >= word2.row:
                            self.connections.append(Connection(word1, word2, word1.col, word2.row))

    # ---------------AC-3-algorithmus----------------------------------------------------------------------------------------
    def ac_3(self):
        queue = self.arc_consistency.copy()

        while queue:
            xi, xj = queue.pop()
            if self.revise(xi, xj):
                if len(di) == 0:
                    return False

                for xk in self.neighbors[xi]:
                    if xk != xj and [xk, xj] not in queue:
                        queue.append(xk, xi)
        return True

    # def revise(self, xi, xj):
    #     revised = False
    #
    #     for x in di:
    #         if ...:
    #             revised = True
    #
    #     return revised


# -----------------Backtraking-------------------------------------------------------------------------------------------
# def backtraking_search(self):
#     return  self.backtrack()

# def backtrack(self, assignment):
#     if self.test_is_solved(assignment):
#         return assignment
#
#     var = self.select_unassigned_variable(assignment)
#
#     for value in self.order_domain_values(var, assignment):
#         if value is


############################### SERVICE METHODS ###############################

def load_words(path):
    # Loads all words from file
    return open(path, 'r').read().splitlines()


def load_grids(path):
    # Loads empty grids from file
    raw = open(path, 'r').read().split('\n\n')
    per_rows = [grid.rstrip().split('\n') for grid in raw]
    per_char = [[list(row) for row in grid] for grid in per_rows]
    return per_char


################################### SOLVING ###################################


def solve(crossword):
    # Fill the empty spaces in crossword with words
    ### YOUR CODE GOES HERE ###
    crossword.ac_3()
    pass


################################ MAIN PROGRAM #################################

if __name__ == "__main__":
    ## Load data:
    words = load_words('words.txt')
    grids = load_grids('krizovky.txt')

    # ## Examples:
    # dummy_grid = [list(s) for s in ['########', '#      #', '#      #', '#      #', '###    #', '#      #', '########']]
    # cw = CrossWord(dummy_grid)
    # cw.print_grid()  # empty grid
    # print('Positions: ' + str(cw.positions))
    # cw.write_word((2, 1, 5, 'right'), 'hello')
    # cw.write_word((1, 5, 5, 'down'), 'world')
    # cw.write_word((4, 3, 4, 'right'), 'milk')
    # cw.print_grid()  # 3 words already filled in
    # print('Text at position (1,4) down: "' + cw.text_at_pos((1, 4, 5, 'down')) + '"\n\n\n')

    points = [0.5, 1, 1, 1, 1.5, 1.5, 2, 2, 1.5, 2]
    points_so_far = 0
    # Solve crosswords (the last one is a bonus)
    # instead of range(len(grids)) specify in which order do you want your crosswords to be tested
    cw = CrossWord(grids[0], words)
    solve(cw)
    cw.print_grid()
    # for i in range(len(grids)):
    #     print('==== Crossword No.' + str(i + 1) + ' ====')
    #     cw = CrossWord(grids[i], words)
    #     solve(cw)
    #     cw.print_grid()
    #
    #     points_so_far += points[i]
    #     print(f'Given all the solved crosswords are correct, you have so far {points_so_far}'
    #           ' (+ max 3 for code and readme) points!')

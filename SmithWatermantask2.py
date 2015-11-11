import sys
import os

"""
Prints out assembled sequence and saves to output.txt
Provide command line path to file or select from files in input folder

Usage:
python smithwatermantask2.py [input_file]

Example:
python smithwatermantask2.py sequence_input.txt

Example:
python smithwatermantask2.py

    Available Input Files:
    1. input.txt
    2. input2.txt
    3. input3.txt
    4. input4.txt
    5. example.txt
    6. mytest.txt
    Enter Input File Number:
    >>> 4
"""


class SmithWaterman:
    def __init__(self, sequence_a, sequence_b,
                 insertion_cost,
                 deletion_cost,
                 substitution_cost,
                 match_cost):

        # Input Sequences
        self.sequenceA = sequence_a  # Y Sequence
        self.sequenceB = sequence_b  # X Sequence

        # Edit Costs
        self.insert = insertion_cost
        self.delete = deletion_cost
        self.substitution = substitution_cost
        self.match_cost = match_cost

        # Optimal Matrix
        self.optimal = [[0 for x in range(len(self.sequenceB)+1)]
                        for x in range(len(self.sequenceA)+1)]

        # Direction Matrix
        self.direction = [[0 for x in range(len(self.sequenceB)+1)]
                          for x in range(len(self.sequenceA)+1)]

        # Direction Arrows, Direction value in Binary - 3 bits - can be [XYZ] = [UDL] ~ Up, Diagonal, Left
        self.LEFT = 1
        self.DIAGONAL = 2
        self.UP = 4

        self.max_value = 0
        self.max_indices = [0, 0]
        self.relative_position = NotImplemented

    def align(self):
        # Compute insertions and deletions for 1st row and 1st column
        # Set the values of row 0 and column 0
        self.optimal[0][0] = 0
        self.direction[0][0] = self.DIAGONAL

        for i in range(1, len(self.sequenceA)+1):
            self.optimal[i][0] = 0
            self.direction[i][0] = self.UP

        for i in range(1, len(self.sequenceB)+1):
            self.optimal[0][i] = 0
            self.direction[0][i] = self.LEFT

        # Compute the rest of the cells
        for i in range(1, len(self.sequenceA)+1):
            for j in range(1, len(self.sequenceB)+1):

                if self.sequenceA[i-1] == self.sequenceB[j-1]:
                    score_diagonal = self.optimal[i - 1][j - 1] + self.match_cost  # If Symbols Match
                else:
                    score_diagonal = self.optimal[i - 1][j - 1] + self.substitution  # Otherwise Substitute

                score_left = self.optimal[i][j - 1] + self.insert
                score_up = self.optimal[i - 1][j] + self.delete

                # Take the maximum of these scores
                self.optimal[i][j] = max(0,  # Indicates a 'Free Ride' to that cell
                                         score_diagonal,  # Score of going Diagonal
                                         score_left,  # Score of going Left
                                         score_up)  # Score of going Up
                self.direction[i][j] = 0
                if self.optimal[i][j] == score_left:
                    self.direction[i][j] += self.LEFT
                if self.optimal[i][j] == score_diagonal:
                    self.direction[i][j] += self.DIAGONAL
                if self.optimal[i][j] == score_up:
                    self.direction[i][j] += self.UP

                if self.optimal[i][j] > self.max_value:
                    self.max_value = self.optimal[i][j]
                    self.max_indices = [i, j]
                # end of align

    def print_matrices(self):
        """
        Prints out Optimal and Direction Matrices
        """

        """
        Print Optimal Matrix
        """
        print("\n", "_"*7, "Optimal Matrix", "_"*7)
        print("\t\t" + "\t".join(list(self.sequenceB)))
        for i in range(0, len(self.sequenceA)+1):

            if i >= 1:
                print(self.sequenceA[i-1] + '\t', end="")
            else:
                print('\t', end="")
            for j in range(0, len(self.sequenceB)+1):
                print(str(self.optimal[i][j]) + '\t', end=""),
            print("")

        """
        Print Direction Matrix
        """
        print("\n", "_"*7, "Direction Matrix", "_"*7)
        print("\t\t" + "\t".join(list(self.sequenceB)))
        for i in range(0, len(self.sequenceA)+1):
            if i >= 1:
                print(self.sequenceA[i-1] + '\t', end=""),
            else:
                print('\t', end=""),
            for j in range(0, len(self.sequenceB)+1):
                print(str(self.direction[i][j]) + '\t', end=""),
            print("")

    def recurse_tree(self, d, a, tail_top, tail_bottom):
        """
        Follows Arrows Through Direction Matrix From End to Origin
        If a cell has multiple arrows, paths diverge and alignment is
            found for each possible path
        """

        if self.optimal[d][a] == 0:
            self.relative_position = d - a

        else:
            tc = ''
            if d >= 0:
                tc = self.sequenceA[d-1]
            bc = ''
            if a >= 0:
                bc = self.sequenceB[a-1]

            if (self.direction[d][a] & self.LEFT) == self.LEFT:  # If Left Arrow
                self.recurse_tree(d, a - 1, '-' + tail_top, bc + tail_bottom)

            if (self.direction[d][a] & self.DIAGONAL) == self.DIAGONAL:  # If Diagonal Arrow
                self.recurse_tree(d - 1, a - 1, tc + tail_top, bc + tail_bottom)

            if (self.direction[d][a] & self.UP) == self.UP:  # If Up Arrow
                self.recurse_tree(d - 1, a, tc + tail_top, '-' + tail_bottom)

    def get_relative_position(self):
        self.recurse_tree(self.max_indices[0], self.max_indices[1], '', '')


def get_input_directory():
    directory_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(directory_path, "inputs")


def read_sequences():
    try:
        file_name = sys.argv[1]
    except IndexError:
        print("Available Input Files:")
        input_directory = get_input_directory()
        input_file_names = os.listdir(input_directory)
        for i, input_filename in enumerate(input_file_names):
            print(str(i+1) + ".", input_filename)
        file_name = None
        while not file_name:
            try:
                print("Enter Input File Number: ")
                file_index_string = input('>>> ')
                file_index = int(file_index_string) - 1
                file_name = input_file_names[file_index]
                file_name = os.path.join(input_directory, file_name)
            except KeyboardInterrupt:
                file_name = None
            except ValueError:
                file_name = None
            except IndexError:
                file_name = None

    input_file = open(file_name)
    sequences = input_file.read().split("\n")
    sequences = [sequence for sequence in sequences if len(sequence.rstrip()) > 0]
    template = sequences[0]
    shorter_sequences = sequences[1:]
    return template, shorter_sequences


def local_align(sequence1, sequence2):
    smith_waterman = SmithWaterman(sequence_a=sequence1,
                                   sequence_b=sequence2,
                                   insertion_cost=-1,
                                   deletion_cost=-1,
                                   substitution_cost=-3,
                                   match_cost=1)
    smith_waterman.align()
    smith_waterman.get_relative_position()
    return smith_waterman


def merge_strings(string_list):
    while len(string_list) > 1:
        x = string_list[0]
        y = string_list[1]
        z = 0
        for i in range(len(x)+1):
            if x[i:] == y[:len(x)-i]:
                z = x[:i] + y
                break
        string_list = [z] + string_list[2:]
    return string_list[0]


def write_sequence(output_string):
    out_file = open('output\output.txt', 'w')
    out_file.write(output_string)
    out_file.close()


def main():
    template, shorter_sequences = read_sequences()
    sw_list = []
    for sequence in shorter_sequences:
        sw = local_align(template, sequence)
        sw_list.append(sw)
    sw_list.sort(key=lambda x: x.relative_position)

    string_list = [x.sequenceB for x in sw_list]
    output_string = merge_strings(string_list)
    print(output_string)
    write_sequence(output_string)


if __name__ == "__main__":
    main()

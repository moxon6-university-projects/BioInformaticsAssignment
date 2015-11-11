import sys
import os

"""
Reads in two lines at a time from an input file and performs a local
alignment on each of these pairs of lines

Usage:
python smithwatermantask1.py input_file

Example:
python smithwatermantask1.py output4.txt
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

        print("Sequence A:", self.sequenceA)
        print("Sequence B:", self.sequenceB)

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

    def output_matrices(self):
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
            print("\nAligning : %s, %s" % (self.sequenceA, self.sequenceB))
            print(">>> Local Alignment: \n>>> %s\n>>> %s" % (tail_top, tail_bottom))
            print("")

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

    def print_alignments(self):
        self.recurse_tree(self.max_indices[0], self.max_indices[1], '', '')


def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        # Aligns the sequences from the lecture slides
        file_name = "example.txt"

    with open(os.path.join('inputs', file_name)) as input_file:
        while True:
            sequence_a = input_file.readline().rstrip()
            sequence_b = input_file.readline().rstrip()
            if len(sequence_a) > 0 and len(sequence_b) > 0:
                align_sequences(sequence_a, sequence_b)
            else:
                break


def align_sequences(sequence_a, sequence_b):
    print("_"*10, "Sequence Alignment", "_"*10)
    smith_waterman = SmithWaterman(sequence_a=sequence_a,
                                   sequence_b=sequence_b,
                                   insertion_cost=-1,
                                   deletion_cost=-1,
                                   substitution_cost=-3,
                                   match_cost=1)
    smith_waterman.align()
    smith_waterman.output_matrices()
    smith_waterman.print_alignments()
    print("#", "_"*9, "End Sequence Alignment", "_"*9, "#", "\n"*10)

if __name__ == "__main__":
    main()

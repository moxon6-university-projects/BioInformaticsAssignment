#!/usr/bin/python

import sys
import os


class NeedlemanWunch:
    def __init__(self, sequence_a, sequence_b,
                 insertion_cost,
                 deletion_cost,
                 substitution_cost,
                 match_cost):

        # Swap so longer string is along X axis
        if len(sequence_a) > len(sequence_b):
            sequence_a, sequence_b = sequence_b, sequence_a

        # Input Sequences
        self.sequenceA = sequence_a  # Y Sequence
        self.sequenceB = sequence_b  # X Sequence

        print("Sequence A:", sequence_a)
        print("Sequence B:", sequence_a)

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

    def align(self):
        # Compute insertions and deletions for 1st row and 1st column
        # Set the values of row 0 and column 0
        self.optimal[0][0] = 0
        self.direction[0][0] = self.DIAGONAL

        for i in range(1, len(self.sequenceA)+1):
            self.optimal[i][0] = self.optimal[i - 1][0] + self.delete
            self.direction[i][0] = self.UP

        for i in range(1, len(self.sequenceB)+1):
            self.optimal[0][i] = self.optimal[0][i - 1] + self.insert
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

                # Take the minimum of these scores
                self.optimal[i][j] = min(score_diagonal, score_left, score_up)
                self.direction[i][j] = 0
                if self.optimal[i][j] == score_left:
                    self.direction[i][j] += self.LEFT
                if self.optimal[i][j] == score_diagonal:
                    self.direction[i][j] += self.DIAGONAL
                if self.optimal[i][j] == score_up:
                    self.direction[i][j] += self.UP
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

        if d == 0 and a == 0:
            print("___Alignment Output___")
            print(tail_top)
            print(tail_bottom)
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
            # end of recurse tree

    def output_alignments(self):
        print("\n___Outputting Alignments___\n")
        self.recurse_tree(len(self.sequenceA), len(self.sequenceB), '', '')


def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    with open(os.path.join('inputs', file_name)) as input_file:
        sequence_a = input_file.readline().rstrip()
        sequence_b = input_file.readline().rstrip()

    needleman_wunch = NeedlemanWunch(sequence_a=sequence_a,
                                     sequence_b=sequence_b,
                                     insertion_cost=1,
                                     deletion_cost=1,
                                     substitution_cost=1,
                                     match_cost=0)
    needleman_wunch.align()
    needleman_wunch.output_matrices()
    needleman_wunch.output_alignments()

if __name__ == "__main__":
    main()


"""
Example Optimal Matrix
        A   T   C   C   G   A   T
    0   1   2   3   4   5   6   7
T	1	1	1	2	3	4	5	6
G	2	2	2	2	3	3	4	5
C	3	3	3	2	2	3	4	5
A	4	3	4	3	3	3	3	4
T	5	4	3	4	4	4	4	3
A	6	5	4	4	5	5	4	4
T	7	6	5	5	5	6	5	4

Example Direction Matrix
        A   T   C   C   G   A   T
    2   1   1   1   1   1   1   1
T	4	2	2	1	1	1	1	3
G	4	6	6	2	3	2	1	1
C	4	6	6	2	2	1	3	3
A	4	2	7	4	6	2	2	1
T	4	4	2	5	6	6	6	2
A	4	6	4	2	7	6	2	4
T	4	4	6	6	2	7	4	2
"""

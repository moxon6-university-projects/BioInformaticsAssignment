#!/usr/bin/python

import sys
import os


class NeedlemanWunch:
    def __init__(self, sequence_a, sequence_b, i, d, s, m):
        self.sequenceA = sequence_a
        self.sequenceB = sequence_b
        self.insert = i
        self.delete = d
        self.substitution = s
        self.match = m
        
        self.opt = [[0 for x in range(len(self.sequenceB)+1)] for x in range(len(self.sequenceA)+1)]
        self.dir = [[0 for x in range(len(self.sequenceB)+1)] for x in range(len(self.sequenceA)+1)]

        # The allowed directions
        self.LEFT = 1
        self.DIAGONAL = 2
        self.UP = 4

    def align(self):
        # First of all, compute insertions and deletions at 1st row/column
        self.opt[0][0] = 0
        for i in range(1, len(self.sequenceA)+1):
            self.opt[i][0] = self.opt[i - 1][0] + self.delete
        for j in range(1, len(self.sequenceB)+1):
            self.opt[0][j] = self.opt[0][j - 1] + self.insert

        # Set the values of row 0 and column 0
        self.dir[0][0] = 2
        for i in range(1, len(self.sequenceA)+1):
            self.dir[i][0] = 4
        
        for i in range(1, len(self.sequenceB)+1):
            self.dir[0][i] = 1

        # Now compute the rest of the cells
        for i in range (1, len(self.sequenceA)+1):
            for j in range (1, len(self.sequenceB)+1):
                score_diag = self.opt[i - 1][j - 1]
                if self.sequenceA[i-1] == self.sequenceB[j-1]:
                    score_diag += self.match
                else:
                    score_diag += self.substitution
                score_left = self.opt[i][j - 1] + self.insert
                score_up = self.opt[i - 1][j] + self.delete
                # we take the minimum
                self.opt[i][j] = min(score_diag, score_left, score_up)
                self.dir[i][j] = 0
                if self.opt[i][j] == score_left:
                    self.dir[i][j] += self.LEFT
                if self.opt[i][j] == score_diag:
                    self.dir[i][j] += self.DIAGONAL
                if self.opt[i][j] == score_up:
                    self.dir[i][j] += self.UP
                # end of align

    def output_matrices(self):
        for j in range(-1, len(self.sequenceB)+1):
            if j >= 1:
                print(self.sequenceB[j-1] + '\t', end=""),
            else:
                print('\t', end="")
        print("\t")
        for i in range(0, len(self.sequenceA)+1):
            if i >= 1:
                print(self.sequenceA[i-1] + '\t', end=""),
            else:
                print('\t', end=""),
            for j in range(0, len(self.sequenceB)+1):
                print(str(self.opt[i][j]) + '\t', end=""),
            print("")
        print("")

        for j in range(-1, len(self.sequenceB)+1):
            if j >= 1:
                print(self.sequenceB[j-1] + '\t', end=""),
            else:
                print('\t', end=""),
        print("")
        # Output directions
    
        for i in range(0, len(self.sequenceA)+1):
            if i >= 1:
                print(self.sequenceA[i-1] + '\t', end=""),
            else:
                print('\t', end=""),
            for j in range(0, len(self.sequenceB)+1):
                print(str(self.dir[i][j]) + '\t', end=""),
            print("")
            # end of output matrix

    def recurse_tree(self, d, a, tail_top, tail_bottom):
        if d == 0 and a == 0:
            print("+")
            print(tail_top)
            print(tail_bottom)
        else:
            tc = ''
            if d >= 0:
                tc = self.sequenceA[d-1]
            bc = ''
            if a >= 0:
                bc = self.sequenceB[a-1]

            if (self.dir[d][a] & self.LEFT) == self.LEFT:  # we go left
                self.recurse_tree(d, a - 1, '-' + tail_top, bc + tail_bottom)

            if (self.dir[d][a] & self.DIAGONAL) == self.DIAGONAL:  # we go diagonal
                self.recurse_tree(d - 1, a - 1, tc + tail_top, bc + tail_bottom)

            if (self.dir[d][a] & self.UP) == self.UP:  # we go up
                self.recurse_tree(d - 1, a, tc + tail_top, '-' + tail_bottom)
            # end of recurse tree

    def output_alignments(self):
        self.recurse_tree(len(self.sequenceA), len(self.sequenceB), '', '')


def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"

    with open(os.path.join('inputs', file_name)) as f:
        sA = f.readline().rstrip()
        sB = f.readline().rstrip()

    print(sA)
    print(sB)

    nw = NeedlemanWunch(sA, sB, 1, 1, 1, 0)
    nw.align()
    nw.output_matrices()
    nw.output_alignments()

if __name__ == "__main__":
    main()


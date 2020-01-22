#!/usr/bin/env python3

"""
Takes methylkit file from stdin, merges the strands, and prints the merged file
"""

import sys

prev_line = "chrBase	chr	base	strand	coverage	freqC	freqT".split("\t")
print("\t".join(map(str, prev_line)))

for line in sys.stdin:
    line = line.strip().split("\t")
    if (prev_line[3], line[3]) == ("F", "R"):
        base = int(line[2])
        prev_base = int(prev_line[2])
        if base - prev_base == 1:
            covg = int(line[4])
            Cs = int(float(line[5]) * covg)
            prev_covg = int(prev_line[4])
            prev_Cs = int(float(prev_line[5]) * prev_covg)
            new_covg = covg + prev_covg
            new_Cs = Cs + prev_Cs
            new_freqC = round(new_Cs / new_covg, 2)
            new_freqT = round(100 - new_freqC, 2)
            prev_line[4] = new_covg
            prev_line[5] = new_freqC
            prev_line[6] = new_freqT
            print("\t".join(map(str, prev_line)))
        else:
            print("\t".join(map(str, prev_line)))
            print("\t".join(map(str, line)))
    elif (prev_line[3], line[3]) == ("F", "F"):
        print("\t".join(map(str, prev_line)))
    elif (prev_line[3], line[3]) == ("R", "R"):
        print("\t".join(map(str, line)))
    prev_line = line

if prev_line[3] == "F":
    print("\t".join(map(str, prev_line)))
#!/usr/bin/env python3

import argparse
import sys
import random


if len(sys.argv) != 2:
	print("Usage: cat <methylkit file> | downsample_methylKit.py <fraction of reads to keep> > <output file>")
	sys.exit()

downsample_number = int(float(sys.argv[1]) * 100)

print(next(sys.stdin).strip())
for line in sys.stdin:
# 	print(line.strip())
	meth = []
	unmeth = []

	line = line.strip().split("\t")

	covg = int(line[4])
	meth_fraction = float(line[5]) / 100
	unmeth_fraction = float(line[6]) / 100
# 	print(covg, meth_fraction, unmeth_fraction)
	
	meth_covg = int(round(covg * meth_fraction))
	unmeth_covg = int(round(covg * unmeth_fraction))
# 	print(meth_covg, unmeth_covg)
	
	meth = [1] * meth_covg
	unmeth = [1] * unmeth_covg
# 	print(meth, unmeth)
	
	for x in range(len(meth)):
		tmp = random.randint(0, 100)
# 		print(tmp)
		if tmp > downsample_number:
# 			print("Removing one methylated coverage")
			meth[x] = 0
	
	for x in range(len(unmeth)):
		tmp = random.randint(0, 100)
# 		print(tmp)
		if tmp > downsample_number:
# 			print("Removing one unmethylated coverage")
			unmeth[x] = 0

# 	print(meth, unmeth)
	
	new_covg = sum(meth) + sum(unmeth)
# 	print(new_covg)
	
	new_meth_fraction = line[5]
	new_unmeth_fraction = line[6]
	
	if new_covg > 0:
		new_meth_fraction = round(float(sum(meth) / new_covg) * 100, 2)
		new_unmeth_fraction = round(float(sum(unmeth) / new_covg) * 100, 2)
# 		print(new_meth_fraction, new_unmeth_fraction)
	
		line[4] = str(new_covg)
		line[5] = str(new_meth_fraction)
		line[6] = str(new_unmeth_fraction)
		print("\t".join(line))
	
	
	
	

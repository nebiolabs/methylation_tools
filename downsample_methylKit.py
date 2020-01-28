#!/usr/bin/env python3

import argparse
import sys
import random


if len(sys.argv) != 2:
	print("Usage: cat <methylkit file> | grep -v chrBase | downsample_methylKit.py <fraction of reads to keep> > <output file>")
	sys.exit()

downsample_len = len(sys.argv[1].split(".")[1]) # Counts number of decimal places, for downsampling precision
downsample_number = int(sys.argv[1].split(".")[1])
downsample_cap = int("".join(["1" ,"".join(["0" for x in range(downsample_len)])])) # An order of magnitude larger than downsample_len


counter = 0
for line in sys.stdin:
	counter += 1
	if counter % 1000000 == 0:
		print("\rProcessed {} lines".format(counter), end = "", file = sys.stderr)
	meth = []
	unmeth = []

	line = line.strip().split("\t")

	covg = int(line[4])
	meth_fraction = float(line[5]) / 100
	unmeth_fraction = float(line[6]) / 100
	
	meth_covg = int(round(covg * meth_fraction))
	unmeth_covg = int(round(covg * unmeth_fraction))
	
	meth = [1] * meth_covg
	unmeth = [1] * unmeth_covg
	
	for x in range(len(meth)):
		tmp = random.randint(0, downsample_cap)
		if tmp > downsample_number:
			meth[x] = 0
	
	for x in range(len(unmeth)):
		tmp = random.randint(0, downsample_cap)
		if tmp > downsample_number:
			unmeth[x] = 0

	new_covg = sum(meth) + sum(unmeth)
	
	new_meth_fraction = line[5]
	new_unmeth_fraction = line[6]
	
	if new_covg > 0:
		new_meth_fraction = round(float(sum(meth) / new_covg) * 100, 2)
		new_unmeth_fraction = round(float(sum(unmeth) / new_covg) * 100, 2)
	
		line[4] = str(new_covg)
		line[5] = str(new_meth_fraction)
		line[6] = str(new_unmeth_fraction)
		print("\t".join(line))
	
	
	
	

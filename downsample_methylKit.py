#!/usr/bin/env python3

import argparse
import sys
import random


if len(sys.argv) == 1:
	print("""Usage: cat <methylkit file> | grep -v chrBase | downsample_methylKit.py --fraction <fraction of reads to keep> > <output file>
			OR
			cat <bedGraph file> | grep -v track | downsample_methylKit.py --fraction <fraction of reads to keep> --bedGraph > <output file>
			""")
	sys.exit()

def argparser():
        parser = argparse.ArgumentParser()
        parser.add_argument("--fraction", required = True, help = "Fraction of reads to keep")
        parser.add_argument("--bedGraph", required = False, action = "store_true", help = "Maximum coverage to include")
        args = parser.parse_args()
        return args

args = argparser()

downsample_len = len(args.fraction.split(".")[1]) # Counts number of decimal places, for downsampling precision
downsample_number = int(args.fraction.split(".")[1])
downsample_cap = int("".join(["1" ,"".join(["0" for x in range(downsample_len)])])) # An order of magnitude larger than downsample_len


def remove_covgs(covg_list):
	my_covg_list = covg_list
	for x in range(len(my_covg_list)):
		tmp_random = random.randint(0, downsample_cap)
		if tmp_random > downsample_number:
			my_covg_list[x] = 0

	return my_covg_list

counter = 0
for line in sys.stdin:
	counter += 1
	if counter % 1000000 == 0:
		print("\rProcessed {} lines".format(counter), end = "", file = sys.stderr)

	line = line.strip().split("\t")

	if args.bedGraph == True:
		meth_covg = int(line[4])
		unmeth_covg = int(line[5])
	else:
		covg = int(line[4])

		meth_fraction = float(line[5]) / 100
		unmeth_fraction = float(line[6]) / 100
		
		meth_covg = int(round(covg * meth_fraction))
		unmeth_covg = int(round(covg * unmeth_fraction))
	
	meth = remove_covgs([1] * meth_covg)
	unmeth = remove_covgs([1] * unmeth_covg)

	new_covg = sum(meth) + sum(unmeth)
	if new_covg > 0:
		if args.bedGraph == True:
			line[3] = str(int(100 * (sum(meth) / new_covg)))
			line[4] = str(sum(meth))
			line[5] = str(sum(unmeth))
		else:
			new_meth_fraction = round(float(sum(meth) / new_covg) * 100, 2)
			new_unmeth_fraction = round(float(sum(unmeth) / new_covg) * 100, 2)
		
			line[4] = str(new_covg)
			line[5] = str(new_meth_fraction)
			line[6] = str(new_unmeth_fraction)
	
		print("\t".join(line))



	
	
	

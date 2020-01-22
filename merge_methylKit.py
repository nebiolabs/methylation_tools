#!/usr/bin/env python3

import sys
import argparse
import time

def argparser():
	parser = argparse.ArgumentParser()
	parser.add_argument("--methylkit", required = False, help = "Concatenated / sorted methylKit file to merge")
	parser.add_argument("--prefix", required = True, help = "Prefix for the output file")
	args = parser.parse_args()
	return args

class MyData:
	# combined	chrom	coord	strand	covg	meth	nonmeth
	# chr1.10469	chr1	10469	F	1	  0.00	100.00
	def __init__(self, combined, chrom, coord, strand, covg, meth, nonmeth):
		self.combined = combined
		self.chrom = chrom
		self.coord = coord
		self.strand = strand
		self.covg = covg
		self.meth = meth
		self.nonmeth = nonmeth

def calculate_Cs(covg, meth):
	Cs = round(covg * (meth / 100))
	
	return Cs
	
def combine_coverages(current_covg, new_covg, current_Cs, new_Cs):
	total_covg = current_covg + new_covg
	total_Cs = current_Cs + new_Cs
	freqC = round(total_Cs / total_covg, 4) * 100
	freqT = 100 - freqC
	
	return total_covg, freqC, freqT

def merge_files(methylkit, prefix):

	ThisLine = MyData(None, None, None, None, None, None, None)
	
	if methylkit != None:
		file = open(methylkit, "r")
	else:
		file = sys.stdin
	out = open("{}_merged.methylKit".format(prefix), "w")
	out.write("chrBase\tchr\tbase\tstrand\tcoverage\tfreqC\tfreqT\n")
	counter = 0
	now = time.time()
	for line in file:
		if "chrBase\tchr\tbase\tstrand\tcoverage\tfreqC\tfreqT" in line or line == "\n":
			continue
		# print(line)
		counter += 1
		if counter % 1000000 == 0:
			print("Processed {} lines in {} seconds".format(counter, time.time() - now))
			now = time.time()
		line = line.strip().split("\t")
		if line[0] == ThisLine.combined:
			current_Cs = calculate_Cs(ThisLine.covg, ThisLine.meth)
			new_Cs = calculate_Cs(int(line[4]), float(line[5]))
			ThisLine.covg, ThisLine.meth, ThisLine.nonmeth = combine_coverages(ThisLine.covg, int(line[4]), current_Cs, new_Cs)
				
		else:
			if ThisLine.combined != None:
				out.write("\t".join(map(str, [ThisLine.combined, ThisLine.chrom, ThisLine.coord, ThisLine.strand, ThisLine.covg, ThisLine.meth, ThisLine.nonmeth])))
				out.write("\n")
			ThisLine = MyData(line[0], line[1], line[2], line[3], int(line[4]), float(line[5]), float(line[6]))
	else:
		out.write("\t".join(map(str, [ThisLine.combined, ThisLine.chrom, ThisLine.coord, ThisLine.strand, ThisLine.covg, ThisLine.meth, ThisLine.nonmeth])))
		out.write("\n")
	
def run_script():
	print("Running script...")
	args = argparser()
	
	if args.methylkit:
		merge_files(args.methylkit, args.prefix)     	        
	else:
		merge_files(None, args.prefix)
        
if __name__ == "__main__":
        run_script()
        print("All done!")
# methylation_tools
A few tools for manipulating methylation call files


# merge_methylkit
Script to merge multiple methylKit files together, e.g., from multiple replicates of one library.

Usage:
```
cat (or zcat) *.methylKit<.gz> | sort -k2,2 -k3,3n | merge_methylKit.py --prefix <prefix for output file>
```
OR
```
paste -d "\n" <(cat file1) <(cat file2) <(cat file3) <etc.> | sort -k2,2 -k3,3n | merge_methylKit.py --prefix <prefix for output file>
```
I'm not sure which is most efficient.

Will create \<prefix>_merged.methylKit as the output.

# merge_cpg_strands
Script to merge the information from both strands of a CpG dinucleotide. Comparable to MethylDackel extract's --mergeContext option

Usage:
```
cat <methylKit file> | merge_cpg_strands.py > <output file>
```

# downsample_methylKit
Script to downsample the observed methylation calls from a methylKit (or bedGraph) file.

Usage:
```
cat <methylkit file> | grep -v chrBase | downsample_methylKit.py --fraction <fraction of reads to keep> > <output file>
```
OR
```
cat <bedGraph file> | grep -v track | downsample_methylKit.py --fraction <fraction of reads to keep> --bedGraph > <output file>
```

This can be used in place of downsampling reads from a fastq/bam before doing methylation calling. The figures below show the similar results between downsampling before or after calling methylation:

Histogram of coverage per site:

![coverage histogram](/images/Coverage_histogram.png)


Histogram of percent methylation per site:

![methylation histogram](/images/percent_methylation_histogram.png)


Histogram of the difference in inferred methylation when downsampling before or after methylation calling:
![percent difference histogram](/images/percent_difference_histogram.png)

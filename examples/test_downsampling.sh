cat example_1.methylKit | grep -v chrBase | ../downsample_methylKit.py --fraction 0.5

cat example.bedGraph | grep -v track | ../downsample_methylKit.py --fraction 0.5 --bedGraph

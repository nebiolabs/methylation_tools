paste -d "\n" <(cat example_1.methylKit) <(cat example_2.methylKit) | sort -k2,2 -k3,3n | ../merge_methylKit.py --prefix test_merging

## Problems found while parsing Bible corpus

1. Some files have content lines marked with # as metadata. (example: [bnp-x-bible.txt](paralleltext-master/bibles/bnp-x-bible.txt)). 
    * Solution: detect such lines with regex, remove leading #.
2. Inconsistent meta naming. Extra spaces at the end, upper/lower case letters are confused in some names.
    * Solution: strip and lowercase all the meta names.
3. One verse have no id. ([mbj-x-bible.txt](paralleltext-master/bibles/mbj-x-bible.txt), line 6863)
    * Solution: idk, ill skip them for now, gonna ask what to do with them
4. A weird line in [ruf-x-bible.txt](paralleltext-master/bibles\ruf-x-bible.txt), line 8
    * `"<<<<<<< HEAD:bibles/corpus/ruf-x-bibile.txt"`
    * Solution: skip
5. Two instances of 58004011 in [luo-x-bible.txt](paralleltext-master/bibles/luo-x-bible.txt)
    * Second one has contents of the missing 58004012. [This translator](glosbe.com/luo/en) helped with this problem
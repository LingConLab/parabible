## Problems found while parsing Bible corpus

1. Some files have content lines marked with # as metadata. (example: [bnp-x-bible.txt](paralleltext-master\bibles\corpus\bnp-x-bible.txt)). 
    * Solution: detect such lines with regex, remove leading #
2. Some files have 
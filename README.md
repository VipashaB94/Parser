# Parsing
This script takes a CFG grammar and a set of sentences and returns all possible parses of those sentences using the CKY algorithm. If the CFG is not already in Chmosky Normal Form, it will be converted before the sentences are parsed, and the new CNF grammar will be written to a file named 'converted_cnf.txt'. The final parses will be written to 'parses.txt'.

CKY.py contains the classes to convert the CFG and for the CKY algorithm. In order to actually parse sentences, run the run_cky.py script. This takes two command line arguments, the first is the file containing the input CFG, and the second is the file containing the sentences to be parsed. So to run the script with the example files provided, you would need: python3 run_cky.py test_cfg.txt sentences.txt.

You may need to update the path to nltk.data in cky.py for the code to run. This line of code can be found below the import statements.

Example files have been provided here to run the script, but it will also work with much larger, more complex files.

Note: the script cannot currently handle CFG files with empty transitions.

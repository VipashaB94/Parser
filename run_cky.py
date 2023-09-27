#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: vipashabansal
"""

from cky import *

import nltk
from nltk import CFG
from nltk import Nonterminal
from nltk import Production
from nltk import data
import sys


def convert_cnf(grammar):
    convert = cnf_converter(grammar)
    convert.all_mixed_rules()
    convert.all_unit_rules()
    convert.all_long_rules()
    start, new_grammar = convert.get_grammar()
    return start, new_grammar

def write_cnf_grammar(start, grammar):
    with open("converted_cnf.txt", "w") as output:
        output.write("%start {} \n".format(start))
        for rule in grammar.productions():
            output.write("{} \n".format(rule))

input_cfg = sys.argv[1]
test_sents = sys.argv[2]

grammar = data.load(input_cfg, 'cfg')

with open(test_sents, "r") as sents:
    sentences = sents.readlines()

#If provided CFG is not in Chomsky Normal Form, convert it
if not grammar.is_chomsky_normal_form():
    start, grammar = convert_cnf(grammar)
    write_cnf_grammar(start, grammar)

#Parse each sentence and print the results
parser = cky_parser(grammar)

with open("parses.txt", 'w') as output:
    for sentence in sentences:
        output.write("{} \n".format(sentence))
        
        count = 0
        words = nltk.word_tokenize(sentence)
        
        #Deal with sentences that contain vocabulary items not covered by the CFG
        try:
            grammar.check_coverage(words)
        except ValueError:
            output.write("Sentence contains vocabulary not covered by the grammar. \n")
            output.write("Number of parses: 0 \n \n")
            continue
        
        #Run CKY parser
        last_ind = len(words)
        backpointers = parser.cky(words, last_ind)
        
        #Print results to file
        for tree in backpointers[0][last_ind]:
            if tree.label() == parser.get_start():
                count += 1
                output.write(str(tree))
                output.write("\n")
        output.write("Number of parses: {} \n \n".format(count))



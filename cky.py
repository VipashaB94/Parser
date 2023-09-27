#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: vipashabansal
"""

import nltk
from nltk import CFG
from nltk import Nonterminal
from nltk import Production
from nltk import data
from nltk import Tree
nltk.data.path.append('/corpora/nltk/nltk-data')


class cnf_converter:

    def __init__(self, grammar):
        self.__grammar = grammar
        self.__start = self.__grammar.start()
        
    def get_grammar(self):
        return self.__start, self.__grammar
    
    def one_mixed_rule(self, rule):
        rhs = rule.rhs()
        new_rhs = []
        productions = []
        for item in rhs:
            new_non = Nonterminal(item) 
            new_rhs.append(new_non)
            it_list = [item]
            new_prod = Production(new_non, it_list)
            if new_prod.is_lexical():
                productions.append(new_prod)
        new_prod_overall = Production(rule.lhs(), new_rhs)
        productions.append(new_prod_overall)

        return productions
    
    def one_unit_rule(self, rule):
        productions = []
        orig_rhs = rule.rhs()
        for prod in self.__grammar.productions():
            if prod.lhs().symbol() == orig_rhs[0].symbol():
                new_prod = Production(rule.lhs(), prod.rhs())
                if len(new_prod.rhs()) == 1 and not new_prod.is_lexical():
                    productions += self.one_unit_rule(new_prod)
                else:
                    productions.append(new_prod)
        return productions
    
    def one_long_rule(self, rule, counter):
        productions = []
        orig_rhs = rule.rhs()
        new_non = Nonterminal("X{}".format(counter))
        counter += 1
        
        new_rhs1 = []
        new_rhs1.append(new_non)
        new_rhs1.append(orig_rhs[-1])
        productions.append(Production(rule.lhs(), new_rhs1))
        
        new_rhs2 = []
        for i in range(0, len(orig_rhs) - 1):
            new_rhs2.append(orig_rhs[i])
        new_prod = Production(new_non, new_rhs2)
        
        if len(new_prod.rhs()) > 2:
            productions2, counter = self.one_long_rule(new_prod, counter)
            productions += productions2
        else:
            productions.append(new_prod)
        
        return productions, counter
    
    def all_mixed_rules(self):
        final_prods = []
        for rule in self.__grammar.productions():
            if rule.is_lexical() and len(rule.rhs()) > 1:
                fixed_prods = self.one_mixed_rule(rule)
                final_prods += fixed_prods
            else:
                final_prods.append(rule)

        self.__grammar = CFG(self.__start, final_prods)
    
    def all_unit_rules(self):
        final_prods2 = []
        for rule in self.__grammar.productions():
            if len(rule.rhs()) == 1 and not rule.is_lexical():
                #print("{} \n".format(rule))
                final_prods2 += self.one_unit_rule(rule)
            else:
                final_prods2.append(rule)

        self.__grammar = CFG(self.__start, final_prods2)
    
    def all_long_rules(self):
        counter = 0
        final_prods3 = []
        for rule in self.__grammar.productions():
            if len(rule.rhs()) > 2:
                new_prods, counter = self.one_long_rule(rule, counter)
                final_prods3 += new_prods
            else:
                final_prods3.append(rule)

        self.__grammar = CFG(self.__start, final_prods3)
    
    
    
class cky_parser:
    
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__start_sym = str(self.__grammar.start())
        
        self.__lex_rules = {}
        self.__nt_rules = {}
        
        for prod in grammar.productions():
            if prod.is_lexical():
                orig_lhs = prod.lhs().symbol()
                orig_rhs = prod.rhs()[0]
                #orig_rhs becomes key in new dictionary
                lhs_asvalue = self.__lex_rules.get(orig_rhs, [])
                lhs_asvalue.append(orig_lhs)
                self.__lex_rules.update({orig_rhs: lhs_asvalue})
                
            else:
                orig_lhs = prod.lhs().symbol()
                orig_rhs1 = prod.rhs()[0].symbol()
                orig_rhs2 = prod.rhs()[1].symbol()
                rhs_asStr = "{} {}".format(orig_rhs1, orig_rhs2)
                #orig_rhs becomes key in new dictionary
                lhs_asvalue = self.__nt_rules.get(rhs_asStr, [])
                lhs_asvalue.append(orig_lhs)
                self.__nt_rules.update({rhs_asStr: lhs_asvalue})
    
    def get_start(self):
        return self.__start_sym
    
    def cky(self, sent, n): 
        #Build parse table
        parse = [[ set() for i in range(n+1)] for i in range(n+1)]
        
        #Build backpointer table
        backpointers = [[ [] for i in range(n+1)] for i in range(n+1)]
        
        for j in range(1, n + 1):
            word = sent[j - 1]
            nts = self.__lex_rules[word]

            for nt in nts:
                parse[j - 1][j].add(nt)
                backpointers[j - 1][j].append(Tree(nt, [word]))
            
            for i in range(j - 2, -1, -1):
                
                for k in range(i + 1, j):
                    for item in parse[i][k]:
                        for obj in parse[k][j]:
                            rule = "{} {}".format(item, obj)
                            lhs = self.__nt_rules.get(rule, [])

                            if lhs:
                                for thing in lhs:
                                    parse[i][j].add(thing)
                                    
                                    left_backs = backpointers[i][k]
                                    left_children = []
                        
                                    for tree in left_backs:
                                        if tree.label() == item:
                                            left_children.append(tree)
                                    
                                    right_backs = backpointers[k][j]
                                    right_children = []
                                    for tree in right_backs:
                                        if tree.label() == obj:
                                            right_children.append(tree)

                                    for ltree in left_children:
                                        for rtree in right_children:
                                                backpointers[i][j].append(Tree(thing, [ltree, rtree]))
                    
        return backpointers
    
    
    
            
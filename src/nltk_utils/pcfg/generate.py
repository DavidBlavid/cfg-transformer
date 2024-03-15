import nltk
from nltk import PCFG
import random
import itertools

from nltk_utils.utils import to_pcfg


# example grammar
# S -> A B [1.0]
# A -> "a" [0.5] | A A [0.5]
# B -> "b" [0.5] | B A [0.5]


# this grammar can be used to generate a random grammar
# before generating rules, insert terminal and nonterminal symbols
meta_grammar = [
'S -> RULE [1.0]',
'RULE -> NONTERMINAL " -> " CONTENT_PROB [1.0]',
'CONTENT_PROB -> CONTENT " [" PROBABILITY "]" [1.0]',
'CONTENT -> TERMINAL_PRE [0.25]',
'CONTENT -> NONTERMINAL " " TERMINAL_PRE [0.25]',
'CONTENT -> NONTERMINAL [0.25]',
'CONTENT -> NONTERMINAL " " NONTERMINAL [0.25]',
'TERMINAL_PRE -> "#" TERMINAL "#" [1.0]',    # "#" gets replaced with double quotes later
'PROBABILITY -> "+" [1.0]',                   # "+" gets replaced with a proper probability later
# 'TERMINAL -> "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"',
# 'NONTERMINAL -> "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"',
]

# generate a random valid sentence from the grammar
def generate_sentence_pcfg(grammar: str | nltk.PCFG, join_char=' '):

    # how often to try to generate a valid sentence
    # if we fail, we raise a ValueError
    max_tries = 5

    # how often to try to expand a non-terminal
    # after this many iterations, we give up and try again
    max_iterations = 10000

    # Ensure the grammar is a PCFG object
    grammar = to_pcfg(grammar)

    for current_try in range(max_tries):

        current_iteration = 0
        sentence = [grammar.start()]

        # as long as there are non-terminals in the sentence
        while any(nltk.grammar.is_nonterminal(symbol) for symbol in sentence):

            # find the non-terminals
            non_terminals = [i for i, symbol in enumerate(sentence) if nltk.grammar.is_nonterminal(symbol)]

            if not non_terminals:
                break  # we are done, there are only non-terminals in the sentence

            # randomly choose a non-terminal to expand
            nt_index = random.choice(non_terminals)
            symbol = sentence[nt_index]

            # randomly choose a production for the non-terminal
            # this is weighted by the probability of the production
            productions = grammar.productions(lhs=symbol)
            production = random.choices(productions, weights=[p.prob() for p in productions])[0]

            # replace the non-terminal with the production
            sentence = sentence[:nt_index] + list(production.rhs()) + sentence[nt_index+1:]

            # avoid infinite loops
            current_iteration += 1
            if current_iteration > max_iterations:
                break
        
        # if the sentence is valid, return it
        if not any(nltk.grammar.is_nonterminal(symbol) for symbol in sentence):
            return join_char.join(str(symbol) for symbol in sentence)

    raise ValueError("The grammar is too complex to generate a valid sentence.")

# this function generates a random grammar
def generate_pcfg(terminals, nonterminals, n_rules=5):
    assert n_rules >= len(nonterminals), "There must be at least as many rules as nonterminals (n_rules >= len(nonterminals))"

    meta_rules = meta_grammar.copy()

    terminal_prob = 1.0 / len(terminals)
    nonterminal_prob = 1.0 / len(nonterminals)

    # generate rules for terminals
    for terminal in terminals:
        rule = f'TERMINAL -> "{terminal}" [{terminal_prob}]'
        meta_rules.append(rule)
    
    # generate rules for nonterminals
    for nonterminal in nonterminals:
        rule = f'NONTERMINAL -> "{nonterminal}" [{nonterminal_prob}]'
        meta_rules.append(rule)

    # generate rules
    random_rules = []

    # the first n_nonterminal rules start with the nonterminals
    # so that every nonterminal has at least one rule
    for nonterminal in nonterminals:
        # generate one CONTENT and build the rule like this:
        random_content = generate_sentence_pcfg(meta_rules, join_char='')
        # replace the first character of the content with the nonterminal
        random_rule = nonterminal + random_content[1:]

        # replace all '#' with '""
        random_rule = random_rule.replace('#', '"')

        random_rules.append(random_rule)

    while len(random_rules) < n_rules:
        random_rule = generate_sentence_pcfg(meta_rules, join_char='')

        if random_rule not in random_rules:
            random_rule = random_rule.replace('#', '"')
            random_rules.append(random_rule)

    finished_nonterminals = []
    finished_rules = []

    # now we assign probabilities to the rules
    for nonterminal in nonterminals:

        if nonterminal in finished_nonterminals:
            # the nonterminal already has a probability
            continue

        # get all rules that start with the same nonterminal
        rules = [r for r in random_rules if r[0] == nonterminal]

        # the sum of the probabilities of all rules that start with the same nonterminal
        prob_sum = 0

        # assign probabilities to the rules
        for j in range(len(rules)):

            # the current rule
            rule = rules[j]

            if not '[+]' in rule:
                # the rule already has a probability
                continue

            # the next random number is between 0 and 1
            # we use this to assign a probability to the rule
            if j < len(rules) - 1:
                prob = random.random() * (1 - prob_sum)
            else:
                prob = 1 - prob_sum
            
            prob_sum += prob

            rule = rule.replace('+', str(prob))
            finished_rules.append(rule)
        
        finished_nonterminals.append(nonterminal)

    # sort the rules
    finished_rules.sort()

    # add the starting rule to the beginning of the list
    starting_rule = 'S -> ' + nonterminals[0] + ' [1.0]'
    finished_rules.insert(0, starting_rule)
    
    # convert the rules to a string
    finished_rules = '\n'.join(finished_rules)

    return finished_rules

# checks if a sentence is in the grammar
def sentence_in_pcfg(sentence: str, grammar: str | nltk.CFG) -> bool:
    
    # Ensure the grammar is an CFG object
    grammar = to_pcfg(grammar)
    
    # split the sentence into a char array
    tokens = list(sentence)
    
    # Initialize the parser with the given grammar
    parser = nltk.parse.EarleyChartParser(grammar)
    
    # Attempt to parse the tokenized sentence
    try:
        # Generate all possible parse trees for the sentence
        for parse in parser.parse(tokens):
            # If at least one parse tree is found, the sentence can be generated by the grammar
            return True
    except ValueError as e:
        # Catch and handle the case where the sentence contains tokens not in the grammar
        return False
    
    # If no parse trees are found, the sentence cannot be generated by the grammar
    return False

# a generator that generates all valid strings for a given grammar until a given length
def generate_sentences_pcfg(terminals, grammar: str | nltk.CFG, max_length=5):
    
    # Ensure the grammar is an CFG object
    grammar = to_pcfg(grammar)

    # Iterate over all lengths of strings
    for length in range(1, max_length + 1):
        # Generate all combinations with repetition of the current length
        for word in itertools.product(terminals, repeat=length):
            # Join the characters to form a string
            sentence = ''.join(word)

            # Check if the sentence is in the grammar
            in_grammar = sentence_in_pcfg(sentence, grammar)

            # If the sentence is in the grammar, yield it
            if in_grammar:
                yield sentence
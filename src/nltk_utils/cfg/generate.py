import nltk
import random
import itertools

from nltk_utils.utils import to_cfg

# this grammar can be used to generate a random grammar
# before generating rules, insert terminal and nonterminal symbols
meta_grammar = [
'S -> RULE',
'RULE -> NONTERMINAL " -> " CONTENT',
'CONTENT -> CONTENT " | " CONTENT | TERMINAL_PRE | TERMINAL_PRE " " NONTERMINAL | NONTERMINAL " " TERMINAL_PRE | NONTERMINAL " " NONTERMINAL | TERMINAL_PRE " " TERMINAL_PRE | TERMINAL_PRE " " NONTERMINAL " " TERMINAL_PRE',
'TERMINAL_PRE -> "#" TERMINAL "#" ',    # "#" gets replaced with double quotes later
# 'TERMINAL -> "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"',
# 'NONTERMINAL -> "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"',
]

# generate a random valid sentence from the grammar
def generate_random_sentence(grammar: str | nltk.CFG, join_char=' '):

    # how often to try to generate a valid sentence
    # if we fail, we raise a ValueError
    max_tries = 5

    # how often to try to expand a non-terminal
    # after this many iterations, we give up and try again
    max_iterations = 10000

    # Ensure the grammar is an CFG object
    grammar = to_cfg(grammar)

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
            productions = grammar.productions(lhs=symbol)
            
            production = random.choice(productions)

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
def generate_random_grammar(terminals, nonterminals, n_rules=5):
    assert n_rules >= len(nonterminals), "There must be at least as many rules as nonterminals (n_rules >= len(nonterminals))"

    meta_rules = meta_grammar.copy()

    # generate rules for terminals
    for terminal in terminals:
        rule = f'TERMINAL -> "{terminal}"'
        meta_rules.append(rule)
    
    # generate rules for nonterminals
    for nonterminal in nonterminals:
        rule = f'NONTERMINAL -> "{nonterminal}"'
        meta_rules.append(rule)

    # generate rules
    random_rules = []

    # the first n_nonterminal rules start with the nonterminals
    # so that every nonterminal has at least one rule
    for nonterminal in nonterminals:
        # generate one CONTENT and build the rule like this:
        random_content = generate_random_sentence(meta_rules, join_char='')
        # replace the first character of the content with the nonterminal
        random_rule = nonterminal + random_content[1:]

        # replace all '#' with '""
        random_rule = random_rule.replace('#', '"')

        random_rules.append(random_rule)

    while len(random_rules) < n_rules:
        random_rule = generate_random_sentence(meta_rules, join_char='')

        if random_rule not in random_rules:
            random_rule = random_rule.replace('#', '"')
            random_rules.append(random_rule)
    
    # sort the rules
    random_rules.sort()

    # add the starting rule to the beginning of the list
    starting_rule = 'S -> ' + nonterminals[0]
    random_rules.insert(0, starting_rule)
    
    # convert the rules to a string
    random_rules = '\n'.join(random_rules)

    return random_rules

# checks if a sentence is in the grammar
def sentence_in_grammar(sentence: str, grammar: str | nltk.CFG) -> bool:
    
    # Ensure the grammar is an CFG object
    grammar = to_cfg(grammar)
    
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
def generate_valid_strings(terminals, grammar: str | nltk.CFG, max_length=5):
    
    # Ensure the grammar is an CFG object
    grammar = to_cfg(grammar)

    # Iterate over all lengths of strings
    for length in range(1, max_length + 1):
        # Generate all combinations with repetition of the current length
        for word in itertools.product(terminals, repeat=length):
            # Join the characters to form a string
            sentence = ''.join(word)

            # Check if the sentence is in the grammar
            in_grammar = sentence_in_grammar(sentence, grammar)

            # If the sentence is in the grammar, yield it
            if in_grammar:
                yield sentence
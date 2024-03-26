from nltk_utils.datasets import generate_documents_pcfg, save_documents, save_grammar
from nltk_utils.pcfg.generate import generate_pcfg, generate_sentence_pcfg, sentence_in_pcfg
from nltk_utils.utils import to_pcfg, generate_nonterminals, generate_terminals
from nltk_utils.graphs import is_transient, has_unproductive_rules


# parameters for the PCFG
N_TERMINALS = 20
N_NONTERMINALS = 10
N_RULES = 20
PROB_TERMINAL = 0.6

# how often to try generating
TRIES = 1000

# translate into a list of terminal and nonterminal chars
terminals = generate_terminals(N_TERMINALS)
nonterminals = generate_nonterminals(N_NONTERMINALS)


counter = 0 # count how many grammars were generated until one with no unproductive rules was found

# generate pcfgs, until one is found that has no unproductive rules
while counter < TRIES:
    # generate a random pcfg
    grammar = generate_pcfg(terminals, nonterminals, N_RULES, PROB_TERMINAL)
    # check if the pcfg has unproductive rules
    if not has_unproductive_rules(grammar):
        break
    counter += 1

if counter == 1000:
    print(f"Could not generate a grammar in {TRIES} tries. Exiting.")
    exit()

print(f"Generated grammar after {counter} tries.")
print(grammar)

# save the grammar
save_grammar(grammar)

# generate sentences from the grammar
n_sentences = 10

print()
print("Sample Sentences:")
for i in range(n_sentences):
    sentence = generate_sentence_pcfg(grammar)
    print(sentence)
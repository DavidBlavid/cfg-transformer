import nltk
import os
from tqdm import tqdm

from nltk_utils.utils import generate_nonterminals, generate_terminals, to_grammar
from nltk_utils.graphs import is_transient
from nltk_utils.pcfg.generate import generate_pcfg, generate_sentence_pcfg

# Saving documents
def generate_document_pcfg(grammar, n_sentences=5, token_join_char=' ', sentence_join_char='.'):
    """Generate a document from the grammar by generating sentences."""
    sentences = [generate_sentence_pcfg(grammar, join_char=token_join_char) for _ in range(n_sentences)]
    return sentence_join_char.join(sentences) + sentence_join_char

def generate_documents_pcfg(grammar, n_documents=5, n_sentences=5, token_join_char=' ', sentence_join_char='.', filename_prefix='document'):
    """Generate multiple documents from the grammar and save them to files."""
    for i in tqdm(range(n_documents)):
        document = generate_document_pcfg(grammar, n_sentences, token_join_char, sentence_join_char)
        filename = f'{filename_prefix}_{i+1}.txt'
        save_document(document, filename)

def save_document(document, filename):
    """Save the document to a file."""

    # create the folder if it does not exist
    if not os.path.exists('documents'):
        os.makedirs('documents')

    with open('documents/' + filename, 'w') as file:
        file.write(document)

def save_documents(documents, suffix: str = "default"):
    with open(f'documents/documents_{suffix}.txt', "w") as f:
        f.write(str(documents))

# Saving/Loading Grammars
def save_grammar_standardized_pcfg(n_terminals: int = 5, n_nonterminals: int = 5, n_rules: int = 5, prob_terminal: float = 0.5):

    # generate the grammar
    terminals = generate_terminals(n_terminals)
    nonterminals = generate_nonterminals(n_nonterminals)

    grammar = None
    while grammar is None or is_transient(grammar):
        grammar = generate_pcfg(terminals, nonterminals, n_rules, prob_terminal)

        if is_transient(grammar):
            print("Transient grammar, retrying...")

    print(grammar)

    suffix = f"{n_terminals}_{n_nonterminals}_{n_rules}"
    save_grammar(grammar, suffix)

def save_grammar(grammar: str) -> None:
    """
    Save a grammar to a file. The filename will be `grammars/grammar_{n_terminals}_{n_nonterminals}_{n_rules}.txt`.
    """

    grammar = to_grammar(grammar)

    # get the number of terminals, nonterminals and rules
    n_terminals = len(set(term for rule in grammar.productions() for term in rule.rhs() if isinstance(term, str)))
    n_nonterminals = len(set(rule.lhs() for rule in grammar.productions())) - 1 # -1 because the start symbol S is not counted
    n_rules = len(grammar.productions()) - 1 # -1 because the start rule S -> A is not counted

    # create the folder if it does not exist
    if not os.path.exists('grammars'):
        os.makedirs('grammars')

    with open(f'grammars/grammar_{n_terminals}_{n_nonterminals}_{n_rules}.txt', "w") as f:
        f.write(str(grammar))

def load_grammar(suffix: str = "default") -> str:
    with open(f'grammars/grammar_{suffix}.txt', "r") as f:
        return f.read()
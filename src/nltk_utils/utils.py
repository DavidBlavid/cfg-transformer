import nltk

def generate_nonterminals(n: int, start='S') -> list[str]:
    """
    Generate a list of uppercase letters to used as nonterminals in a grammar.\\
    I.e. if n=3, the function will return `['A', 'B', 'C']`
    start (`str`): the start symbol of the grammar. Will not be inserted into the list, gets substituted with '1'.
    """
    nonterminals = [chr(65+i) for i in range(n)]

    if start in nonterminals:
        nonterminals.remove(start)
        nonterminals.append('1')

    return nonterminals

def generate_terminals(n: int) -> list[str]:
    """
    Generate a list of lowercase letters to used as terminals in a grammar.\\
    I.e. if n=3, the function will return `['a', 'b', 'c']`
    """
    return [chr(97+i) for i in range(n)]

def to_pcfg(grammar: str | nltk.PCFG) -> nltk.PCFG:
    """
    Transform a string into a PCFG object.
    """

    if isinstance(grammar, str) or isinstance(grammar, list):
        grammar = nltk.PCFG.fromstring(grammar)
    elif not isinstance(grammar, nltk.PCFG):
        raise ValueError("The grammar must be a string or an CFG object.")
    
    return grammar

def to_cfg(grammar: str | nltk.CFG) -> nltk.CFG:
    """
    Transform a string into a CFG object.
    """

    if isinstance(grammar, str) or isinstance(grammar, list):
        grammar = nltk.CFG.fromstring(grammar)
    elif not isinstance(grammar, nltk.CFG):
        raise ValueError("The grammar must be a string or an CFG object.")
    
    return grammar

def to_grammar(grammar: str | nltk.CFG | nltk.PCFG) -> nltk.CFG | nltk.PCFG:
    """
    Automatically translate a string into a CFG or PCFG object.
    """

    if isinstance(grammar, str):
        # if the grammar is a string AND contains '[' or ']', it is a PCFG
        # otherwise, it is a CFG
        if '[' in grammar or ']' in grammar:
            grammar = to_pcfg(grammar)
        else:
            grammar = to_cfg(grammar)
    
    return grammar
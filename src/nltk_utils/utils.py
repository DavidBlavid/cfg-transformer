import nltk

def generate_nonterminals(n: int):
    """
    Generate a list of uppercase letters to used as nonterminals in a grammar.\\
    I.e. if n=3, the function will return ['A', 'B', 'C']
    """
    return [chr(65+i) for i in range(n)]

def generate_terminals(n: int):
    """
    Generate a list of lowercase letters to used as terminals in a grammar.\\
    I.e. if n=3, the function will return ['a', 'b', 'c']
    """
    return [chr(97+i) for i in range(n)]

def to_pcfg(grammar: str | nltk.PCFG):
    """
    Transform a string into a PCFG object.
    """

    if isinstance(grammar, str) or isinstance(grammar, list):
        grammar = nltk.PCFG.fromstring(grammar)
    elif not isinstance(grammar, nltk.PCFG):
        raise ValueError("The grammar must be a string or an CFG object.")
    
    return grammar

def to_cfg(grammar: str | nltk.CFG):
    """
    Transform a string into a CFG object.
    """

    if isinstance(grammar, str) or isinstance(grammar, list):
        grammar = nltk.CFG.fromstring(grammar)
    elif not isinstance(grammar, nltk.CFG):
        raise ValueError("The grammar must be a string or an CFG object.")
    
    return grammar
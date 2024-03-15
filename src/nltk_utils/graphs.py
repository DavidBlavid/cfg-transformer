from collections import defaultdict
from nltk_utils.utils import to_cfg, to_pcfg
import nltk

# returns true, if the grammar will loop endlessly
# implemented by checking whether the graph of the rules is transient
def build_transition_graph(grammar: str | nltk.CFG | nltk.PCFG):
    """Build a transition graph from the grammar for Markov chain analysis."""

    if type(grammar) == str:
        # if the grammar is a string AND contains '[' or ']', it is a PCFG
        # '[' and ']' are used to denote the probabilities of the rules
        if '[' in grammar or ']' in grammar:
            grammar = to_pcfg(grammar)
        else:
            grammar = to_cfg(grammar)
    
    graph = defaultdict(list)
    for production in grammar.productions():
        lhs = str(production.lhs())
        rhs_symbols = [str(rhs) for rhs in production.rhs() if nltk.grammar.is_nonterminal(rhs)]
        graph[lhs].extend(rhs_symbols)
    return graph

def find_reachable_states(graph, start='S'):
    """Find all states reachable from the start symbol using DFS."""
    reachable = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current not in reachable:
            reachable.add(current)
            stack.extend(graph[current])
    return reachable

def find_absorbing_states(grammar: str | nltk.CFG | nltk.PCFG):
    """Identify terminal symbols (absorbing states) in the grammar."""
    return {str(production.lhs()) for production in grammar.productions() if all(not nltk.grammar.is_nonterminal(rhs) for rhs in production.rhs())}

def is_transient(grammar: str | nltk.CFG | nltk.PCFG):
    """Check if the grammar is transient using Markov chain analysis."""
    
    if type(grammar) == str:
        # if the grammar is a string AND contains '[' or ']', it is a PCFG
        # '[' and ']' are used to denote the probabilities of the rules
        if '[' in grammar or ']' in grammar:
            grammar = to_pcfg(grammar)
        else:
            grammar = to_cfg(grammar)
    
    graph = build_transition_graph(grammar)
    absorbing_states = find_absorbing_states(grammar)
    reachable_states = find_reachable_states(graph)
    
    # Initialize all non-terminals as transient until proven otherwise
    transient = {node: True for node in graph}
    
    # Markov chain analysis: Check reachability of absorbing states
    for start in graph:
        visited = set()
        stack = [start]

        # check if start is a reachable state
        # if not, we will never generate it
        # we can ignore it and give it the value True
        if start not in reachable_states:
            transient[start] = True
            continue

        while stack:
            current = stack.pop()
            if current in absorbing_states:
                break  # Found path to absorbing state
            if current not in visited:
                visited.add(current)
                stack.extend(graph[current])
        else:
            transient[start] = False  # No path to absorbing state found
    
    return all(transient.values())

def print_graph(grammar):

    if type(grammar) == str:
        # if the grammar is a string AND contains '[' or ']', it is a PCFG
        # '[' and ']' are used to denote the probabilities of the rules
        if '[' in grammar or ']' in grammar:
            grammar = to_pcfg(grammar)
        else:
            grammar = to_cfg(grammar)
    
    graph = build_transition_graph(grammar)
    reachable_states = find_reachable_states(graph, start='S')
    absorbing_states = find_absorbing_states(grammar)
    transient = is_transient(grammar)

    print("Graph:", graph)
    print("Reachable states:", reachable_states)
    print("Absorbing states:", absorbing_states)
    print("Is transient:", transient)
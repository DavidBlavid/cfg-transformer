from collections import defaultdict
from nltk_utils.utils import to_grammar
import nltk
from networkx import DiGraph, simple_cycles


def build_transition_graph(grammar: str | nltk.CFG | nltk.PCFG) -> dict[str, list[str]]:
    """
    Build a transition graph from the grammar for Markov chain analysis.
    This version includes all rules in the graph.
    """

    grammar = to_grammar(grammar)
    
    graph = defaultdict(list)
    for production in grammar.productions():
        lhs = str(production.lhs())
        rhs_symbols = [str(rhs) for rhs in production.rhs() if nltk.grammar.is_nonterminal(rhs)]
        graph[lhs].extend(rhs_symbols)
    return graph

def build_transient_transition_graph(grammar: str | nltk.CFG | nltk.PCFG) -> dict[str, list[str]]:
    """
    Build a transition graph from the grammar for Markov chain analysis.
    This version removes rules with self-loops and duplicates in the graph.
    """

    grammar = to_grammar(grammar)
    
    graph = defaultdict(list)
    for production in grammar.productions():
        lhs = str(production.lhs())
        rhs_symbols = [str(rhs) for rhs in production.rhs() if nltk.grammar.is_nonterminal(rhs)]

        # remove duplicates
        rhs_symbols = list(set(rhs_symbols))

        # only append if lhs is not in rhs_symbols
        if lhs not in rhs_symbols and len(rhs_symbols) > 0:
            graph[lhs].append(rhs_symbols)
    
    # append empty list for non-terminal symbols without rules
    for production in grammar.productions():
        lhs = str(production.lhs())
        if lhs not in graph:
            graph[lhs] = []
        
    return graph

def get_reachable_states(graph, start='S') -> set[str]:
    """Find all states reachable from the start symbol using DFS."""
    reachable = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current not in reachable:
            reachable.add(current)
            rules = graph[current]
            for rule in rules:
                stack.extend(rule)
    return reachable

def get_unreachable_states(graph, start='S') -> set[str]:
    """Find all states that are not reachable from the start symbol."""
    reachable = get_reachable_states(graph, start=start)
    return set(graph.keys()) - reachable

def find_absorbing_states(grammar: str | nltk.CFG | nltk.PCFG) -> set[str]:
    """Identify terminal symbols (absorbing states) in the grammar."""
    return {str(production.lhs()) for production in grammar.productions() if all(not nltk.grammar.is_nonterminal(rhs) for rhs in production.rhs())}


def get_unproductive_rules(grammar: str | nltk.CFG | nltk.PCFG, start='S'):
    """
    Return the unproductive rules of a grammar.
    See here https://zerobone.net/blog/cs/non-productive-cfg-rules/
    """

    grammar = to_grammar(grammar)
    graph = build_transition_graph(grammar)
    unreachable_states = set(nltk.Nonterminal(state) for state in get_unreachable_states(graph, start=start))

    # Initialize the set of productive non-terminals with those that directly produce terminals
    productive = set()
    for production in grammar.productions():
        if all(isinstance(sym, str) or not isinstance(sym, nltk.Nonterminal) for sym in production.rhs()):
            productive.add(production.lhs())

    # Iteratively update the set of productive non-terminals
    changes = True
    while changes:
        changes = False
        for production in grammar.productions():
            if production.lhs() not in productive:
                if all(sym in productive or not isinstance(sym, nltk.Nonterminal) for sym in production.rhs()):
                    productive.add(production.lhs())
                    changes = True

    # Check if there are any non-terminals that are not in the productive set
    non_productive = set(production.lhs() for production in grammar.productions()) - productive

    # add all unreachable states to the non-productive set
    non_productive.update(unreachable_states)

    # The grammar has unproductive rules if the non_productive set is not empty
    return non_productive

def has_unproductive_rules(grammar: str | nltk.CFG | nltk.PCFG, start='S') -> bool:
    """Returns True if a grammar has at least one unproductive rule."""
    return bool(get_unproductive_rules(grammar, start=start))

def is_transient(grammar: str | nltk.CFG | nltk.PCFG, start='S') -> bool:
    """
    Check if a grammar is transient, meaning that the start symbol will always be reduced into a terminal string.
    A grammar is transient iff its unproductive rules are the unreachable states.
    If a grammar is non-transient, it is cyclic and can never be reduced to a terminal string.
    """

    grammar = to_grammar(grammar)
    graph = build_transition_graph(grammar)

    unreachable_states = set(nltk.Nonterminal(state) for state in get_unreachable_states(graph, start=start))
    unproductive_rules = get_unproductive_rules(grammar)

    return unproductive_rules == unreachable_states

def print_graph(grammar, start='S') -> None:
    """
    Print the transition graph, reachable states, absorbing states, and unproductive rules of a grammar.
    """

    grammar = to_grammar(grammar)
    
    graph = build_transition_graph(grammar)
    reachable_states = get_reachable_states(graph, start=start)
    unreachable_states = get_unreachable_states(graph, start=start)
    absorbing_states = find_absorbing_states(grammar)
    unproductive_rules = [str(rule) for rule in get_unproductive_rules(grammar)]
    transient = is_transient(grammar)

    # sort the lists
    reachable_states = sorted(reachable_states)
    unreachable_states = sorted(unreachable_states)
    absorbing_states = sorted(absorbing_states)
    unproductive_rules = sorted(unproductive_rules)

    print("Graph:             ", graph)
    print("Reachable states:  ", reachable_states)
    print("Unreachable states:", unreachable_states)
    print("Unproductive Rules:", unproductive_rules)
    print("Absorbing states:  ", absorbing_states)
    
    print("Is Transient:      ", transient)
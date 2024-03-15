import nltk
from cfg_utils.graphs import build_transition_graph, find_reachable_states, find_absorbing_states, is_grammar_transient

# Test cases for is_grammar_transient
# True, simple path to terminal
transient_grammar = [
    'S -> A',
    'A -> B',
    'B -> "c"',
]

# False, loop includes A again
nontransient_grammar = [
    'S -> A',
    'A -> B',
    'B -> "c" A',
]

# True, A has an alternative path to "b"
direct_loop_with_terminal = [
    'S -> A',
    'A -> A | "b"',
]

# False, indirect loop without terminal resolution
indirect_loop_without_terminal = [
    'S -> A',
    'A -> B',
    'B -> C',
    'C -> A',
]

# True, despite B and C loop, S can reach terminals through A and D
mixed_starting_nonterminals = [
    'S -> A | D',
    'A -> "a"',
    'B -> C',
    'C -> B',
    'D -> "d"',
]

# True, loops exist but all have escape to terminals
nested_loops_with_escape = [
    'S -> A',
    'A -> B | "e"',
    'B -> C',
    'C -> D | B',
    'D -> "f"',
]

# True, deep nesting but eventually reaches terminal
deeply_nested_structure = [
    'S -> A',
    'A -> B',
    'B -> C',
    'C -> D',
    'D -> E',
    'E -> "g"',
]

# True, complex with multiple paths, some loops, some lead to terminals
complex_grammar_multiple_paths = [
    'S -> A | X',
    'A -> B | "h"',
    'B -> C | "i"',
    'C -> A | "j"',
    'X -> Y',
    'Y -> Z | X',
    'Z -> "k"',
]

if __name__ == "__main__":
                                                                # Expected output
    print(is_grammar_transient(transient_grammar))              # True
    print(is_grammar_transient(nontransient_grammar))           # False
    print(is_grammar_transient(direct_loop_with_terminal))      # True
    print(is_grammar_transient(indirect_loop_without_terminal)) # False
    print(is_grammar_transient(mixed_starting_nonterminals))    # True
    print(is_grammar_transient(nested_loops_with_escape))       # True
    print(is_grammar_transient(deeply_nested_structure))        # True
    print(is_grammar_transient(complex_grammar_multiple_paths)) # True

    grammar = nltk.CFG.fromstring('\n'.join(mixed_starting_nonterminals))
    graph = build_transition_graph(grammar)
    reachable_states = find_reachable_states(graph, start='S')
    absorbing_states = find_absorbing_states(grammar)

    print("Graph:", graph)
    print("Reachable states:", reachable_states)
    print("Absorbing states:", absorbing_states)
    print("Is transient:", is_grammar_transient(mixed_starting_nonterminals))
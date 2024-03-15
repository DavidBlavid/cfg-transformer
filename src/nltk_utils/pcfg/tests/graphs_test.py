import nltk
from nltk_utils.graphs import is_transient, build_transition_graph, find_reachable_states, find_absorbing_states

# Test cases for is_grammar_transient
# True, simple path to terminal
transient_grammar = [
    'S -> A [1.0]',
    'A -> B [1.0]',
    'B -> "c" [1.0]',
]

# False, loop includes A again
nontransient_grammar = [
    'S -> A [1.0]',
    'A -> B [1.0]',
    'B -> "c" A [1.0]',
]

# True, A has an alternative path to "b"
direct_loop_with_terminal = [
    'S -> A [1.0]',
    'A -> A | "b" [1.0]',
]

# False, indirect loop without terminal resolution
indirect_loop_without_terminal = [
    'S -> A [1.0]',
    'A -> B [1.0]',
    'B -> C [1.0]',
    'C -> A [1.0]',
]

# True, despite B and C loop, S can reach terminals through A and D
mixed_starting_nonterminals = [
    'S -> A [0.5] | D [0.5]',
    'A -> "a" [1.0]',
    'B -> C [1.0]',
    'C -> B [1.0]',
    'D -> "d" [1.0]',
]

# True, loops exist but all have escape to terminals
nested_loops_with_escape = [
    'S -> A [1.0]',
    'A -> B [0.5] | "e" [0.5]',
    'B -> C [1.0]',
    'C -> D [0.5] | B [0.5]',
    'D -> "f" [1.0]',
]

# True, deep nesting but eventually reaches terminal
deeply_nested_structure = [
    'S -> A [1.0]',
    'A -> B [1.0]',
    'B -> C [1.0]',
    'C -> D [1.0]',
    'D -> E [1.0]',
    'E -> "g" [1.0]',
]

# True, complex with multiple paths, some loops, some lead to terminals
complex_grammar_multiple_paths = [
    'S -> A [0.5] | X [0.5]',
    'A -> B [0.5] | "h" [0.5]',
    'B -> C [0.5] | "i" [0.5]',
    'C -> A [0.5] | "j" [0.5]',
    'X -> Y [1.0]',
    'Y -> Z [0.5] | X [0.5]',
    'Z -> "k" [1.0]',
]

if __name__ == "__main__":
                                                                # Expected output
    print(is_transient(transient_grammar))              # True
    print(is_transient(nontransient_grammar))           # False
    print(is_transient(direct_loop_with_terminal))      # True
    print(is_transient(indirect_loop_without_terminal)) # False
    print(is_transient(mixed_starting_nonterminals))    # True
    print(is_transient(nested_loops_with_escape))       # True
    print(is_transient(deeply_nested_structure))        # True
    print(is_transient(complex_grammar_multiple_paths)) # True

    grammar_string = '\n'.join(complex_grammar_multiple_paths)

    print_graph(grammar_string)
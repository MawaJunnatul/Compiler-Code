def eliminate_left_recursion(grammar):
    non_terminals = set()
    productions = {}

    # Parsing the input grammar
    for production in grammar:
        non_terminal, production_rules = production.split("->")
        non_terminals.add(non_terminal.strip())
        productions[non_terminal.strip()] = [rule.strip().split() for rule in production_rules.split("|")]

    # Resultant grammar after left recursion elimination
    new_grammar = {}

    for non_terminal in non_terminals:
        new_productions = []
        alpha_productions = []
        for production in productions[non_terminal]:
            if production[0] == non_terminal:
                alpha_productions.append(production[1:])
            else:
                new_productions.append(production + [f"{non_terminal}'"])

        if alpha_productions:
            new_non_terminal = f"{non_terminal}'"
            new_productions.append(["ε"])
            for alpha_production in alpha_productions:
                new_productions.append(alpha_production + [f"{non_terminal}'"])

            new_grammar[new_non_terminal] = new_productions
            new_grammar[non_terminal] = [production[:-1] for production in new_productions if production != ["ε"]]
        else:
            new_grammar[non_terminal] = productions[non_terminal]

    return new_grammar

def print_grammar(grammar):
    for non_terminal, productions in grammar.items():
        print(non_terminal, "→", " | ".join([" ".join(production) for production in productions]))

# Sample Input
sample_input = [
    "E -> E + T | T",
    "T -> T * F | F"
]

# Eliminating left recursion
resultant_grammar = eliminate_left_recursion(sample_input)

# Printing resultant grammar
print("After elimination of left recursion the grammar is:")
print_grammar(resultant_grammar)

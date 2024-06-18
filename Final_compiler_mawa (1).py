import re

# Token types
TOKEN_TYPES = [
    ('NUMBER', r'\d+(\.\d*)?'),   # Integer or decimal number
    ('ADD', r'\+'),               # Addition
    ('SUB', r'-'),                # Subtraction
    ('MUL', r'\*'),               # Multiplication
    ('DIV', r'/'),                # Division
    ('LPAREN', r'\('),            # Left parenthesis
    ('RPAREN', r'\)'),            # Right parenthesis
    ('ID', r'[a-zA-Z_]\w*'),      # Identifiers
    ('ASSIGN', r'='),             # Assignment operator
    ('WHITESPACE', r'\s+'),       # Whitespace
]

# Tokenizer
def tokenize(code):
    tokens = []
    while code:
        match = None
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                text = match.group(0)
                if token_type != 'WHITESPACE':  # Ignore whitespace
                    tokens.append((token_type, text))
                code = code[len(text):]
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens

# Example usage
code = "a = 3 + 5 * (2 - 8) / 2"
tokens = tokenize(code)
print(tokens)
class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

def parse(tokens):
    def parse_expression(index):
        node, index = parse_term(index)
        while index < len(tokens) and tokens[index][0] in ('ADD', 'SUB'):
            op = tokens[index]
            index += 1
            right_node, index = parse_term(index)
            node = ASTNode(op[0], op[1], [node, right_node])
        return node, index

    def parse_term(index):
        node, index = parse_factor(index)
        while index < len(tokens) and tokens[index][0] in ('MUL', 'DIV'):
            op = tokens[index]
            index += 1
            right_node, index = parse_factor(index)
            node = ASTNode(op[0], op[1], [node, right_node])
        return node, index

    def parse_factor(index):
        token = tokens[index]
        if token[0] == 'NUMBER':
            node = ASTNode('NUMBER', token[1])
            return node, index + 1
        elif token[0] == 'ID':
            node = ASTNode('ID', token[1])
            return node, index + 1
        elif token[0] == 'LPAREN':
            index += 1
            node, index = parse_expression(index)
            if tokens[index][0] != 'RPAREN':
                raise SyntaxError("Expected ')'")
            return node, index + 1
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_assignment(index):
        if tokens[index][0] == 'ID' and tokens[index + 1][0] == 'ASSIGN':
            var_name = tokens[index][1]
            index += 2
            expr_node, index = parse_expression(index)
            return ASTNode('ASSIGN', var_name, [expr_node]), index
        return parse_expression(index)

    ast, index = parse_assignment(0)
    if index != len(tokens):
        raise SyntaxError("Unexpected tokens at the end")
    return ast

# Example usage
ast = parse(tokens)
print(ast)
def check_semantics(ast, symbol_table=None):
    if symbol_table is None:
        symbol_table = {}

    if ast.type == 'ASSIGN':
        var_name = ast.value
        expr_node = ast.children[0]
        value = evaluate_expression(expr_node, symbol_table)
        symbol_table[var_name] = value
        return symbol_table
    else:
        evaluate_expression(ast, symbol_table)
    return symbol_table

def evaluate_expression(node, symbol_table):
    if node.type == 'NUMBER':
        return float(node.value)
    elif node.type == 'ID':
        if node.value not in symbol_table:
            raise NameError(f"Undefined variable: {node.value}")
        return symbol_table[node.value]
    elif node.type in ('ADD', 'SUB', 'MUL', 'DIV'):
        left_val = evaluate_expression(node.children[0], symbol_table)
        right_val = evaluate_expression(node.children[1], symbol_table)
        if node.type == 'ADD':
            return left_val + right_val
        elif node.type == 'SUB':
            return left_val - right_val
        elif node.type == 'MUL':
            return left_val * right_val
        elif node.type == 'DIV':
            return left_val / right_val
    else:
        raise ValueError(f"Unexpected node type: {node.type}")

# Example usage
symbol_table = check_semantics(ast)
print(symbol_table)
def generate_ir(ast):
    ir_code = []

    def traverse(node):
        if node.type == 'ASSIGN':
            var_name = node.value
            expr_code = traverse(node.children[0])
            ir_code.append(f"{var_name} = {expr_code}")
            return var_name
        elif node.type == 'NUMBER':
            return node.value
        elif node.type == 'ID':
            return node.value
        elif node.type in ('ADD', 'SUB', 'MUL', 'DIV'):
            left_code = traverse(node.children[0])
            right_code = traverse(node.children[1])
            temp_var = f"t{len(ir_code)}"
            ir_code.append(f"{temp_var} = {left_code} {node.value} {right_code}")
            return temp_var

    traverse(ast)
    return ir_code

# Example usage
ir_code = generate_ir(ast)
print(ir_code)
def optimize_ir(ir_code):
    # Simple optimization example: remove unnecessary assignments
    optimized_code = []
    for line in ir_code:
        if not line.startswith("t"):
            optimized_code.append(line)
    return optimized_code

# Example usage
optimized_ir = optimize_ir(ir_code)
print(optimized_ir)
def generate_machine_code(ir_code):
    machine_code = []
    for line in ir_code:
        machine_code.append(line)  # In a real compiler, this would be translated to actual machine code
    return machine_code




# Example usage
machine_code = generate_machine_code(optimized_ir)
print(machine_code)
code = "h = 12 - 6 * (2 + 8) / 2"

# 1. Lexical Analysis
tokens = tokenize(code)

# 2. Syntax Analysis
ast = parse(tokens)

# 3. Semantic Analysis
symbol_table = check_semantics(ast)

# 4. Intermediate Code Generation
ir_code = generate_ir(ast)

# 5. Optimization (optional)
optimized_ir = optimize_ir(ir_code)

# 6. Code Generation
machine_code = generate_machine_code(optimized_ir)

# Output all phases
print("Tokens:", tokens)
print("\nAbstract Syntax Tree:", ast)
print("\nSymbol Table:", symbol_table)
print("\nIntermediate Code:", ir_code)
print("\nOptimized Intermediate Code:", optimized_ir)
print("\nMachine Code:", machine_code)



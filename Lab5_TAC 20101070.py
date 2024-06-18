import sys
from collections import defaultdict, deque

# Read input from file
with open("input.txt", "r") as f:
    exp = f.readline().rstrip().split(" ")

# Define operator precedence
operator_precedence = {'^': 0, '*': 1, '/': 1, '%': 1, '+': 2, '-': 2}
stack = []
three_address_code = deque()

temp_counter = 1

# Process brackets and generate temporary variables
for char in exp:
    if char == ")":
        temp_stack = []
        while stack and stack[-1] != "(":
            temp_stack.append(stack.pop())
        if stack and stack[-1] == "(":
            stack.pop()
        three_address_code.append((temp_counter, temp_stack[::-1]))
        stack.append("t" + str(temp_counter))
        temp_counter += 1
    else:
        stack.append(char)

three_address_code.append((temp_counter, stack))

result_queue = deque()
temp_mapping = defaultdict(int)
temp_counter = 1

# Generate three-address code
while three_address_code:
    current_entry = three_address_code.popleft()
    index = current_entry[0]
    current_exp = current_entry[1]

    # Update temporary variable mapping
    for i in range(len(current_exp)):
        if current_exp[i][0] == 't':
            current_exp[i] = 't' + str(temp_mapping[int(current_exp[i][1:])])

    while len(current_exp) > 2:
        # Handle sqrt operator
        for i in range(len(current_exp)):
            if current_exp[i] == 'sqrt':
                result_queue.append(("t" + str(temp_counter), "sqrt(" + current_exp[i+1] + ")"))
                current_exp = current_exp[:i] + ["t" + str(temp_counter)] + current_exp[i+2:]
                temp_counter += 1
                break
        
        # Handle exponentiation
        for i in range(len(current_exp)):
            if current_exp[i] == '^':
                temp_exp = deque("*".join([current_exp[i-1]] * int(current_exp[i+1])))
                while len(temp_exp) > 2:
                    for j in range(len(temp_exp)):
                        if temp_exp[j] == '*':
                            result_queue.append(("t" + str(temp_counter), temp_exp[j-1] + "*" + temp_exp[j+1]))
                            temp_exp = deque([*temp_exp[:j-1], "t" + str(temp_counter), *temp_exp[j+2:]])
                            temp_counter += 1
                            break
                current_exp = ["t" + str(temp_counter - 1)] + current_exp[i+2:]
                break
        
        # Handle multiplication, division, and modulus
        flag = False
        for i in range(len(current_exp)):
            if current_exp[i] in ['*', '/', '%']:
                result_queue.append(("t" + str(temp_counter), current_exp[i-1] + current_exp[i] + current_exp[i+1]))
                current_exp = current_exp[:i-1] + ["t" + str(temp_counter)] + current_exp[i+2:]
                temp_counter += 1
                flag = True
                break
        if flag:
            continue
        
        # Handle addition and subtraction
        for i in range(len(current_exp)):
            if current_exp[i] in ['+', '-']:
                if current_exp[i] == '-' and i == 0:
                    result_queue.append(("t" + str(temp_counter), '0' + current_exp[i] + current_exp[i+1]))
                    current_exp = ["t" + str(temp_counter)] + current_exp[i+2:]
                else:
                    result_queue.append(("t" + str(temp_counter), current_exp[i-1] + current_exp[i] + current_exp[i+1]))
                    current_exp = current_exp[:i-1] + ["t" + str(temp_counter)] + current_exp[i+2:]
                temp_counter += 1
                break
        
        # Handle assignment
        for i in range(len(current_exp)):
            if current_exp[i] == '=':
                result_queue.append((current_exp[i-1], current_exp[i+1]))
                current_exp = current_exp[:i-1] + ["t" + str(temp_counter)] + current_exp[i+2:]
                temp_counter += 1
                break

    temp_mapping[index] = len(result_queue)

# Write the result to output.txt
with open("output.txt", "w") as output_file:
    for item in result_queue:
        output_file.write(f"{item[0]} := {item[1]}\n")


import re  # regular expression

hdf= re.compile(r'#include<')

#---------Declare Keywords, operators, punctuation, parenthesis, symbols----------

keywords = ['auto','break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 
            'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 
            'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 
            'unsigned', 'void', 'volatile', 'while']

#---------Operators----------
operators = ['+', '-', '*', '/', '=', '+=', '-=', '==', '<', '>', '<=', '>=']

punctuation = [' ', '	', '.', ',', '\n', ';', '<', '>']

parenthesis = ['(', ')', '{', '}', '[', ']']

symbols = ['!', '@', '#', '$', '%', '&', '^']

#--------------  xxxxx -------------------------


op = []
key = []
pun = []
par = []
identifier = []
constant = []
tokens = [] # "token" list for all tokens
Str = False # check string
Word = False # check word
Cmt = 0  # to reduce comments
token = ''


# ------------- open input file ----------
fp = open("input.txt", 'r')
test = fp.read()


for i in test:

	#Checking comments and remove comments
	if (i == '/'):
		Cmt = Cmt+1

	elif (Cmt == 2):
		if i == '\n':
			token ='' # not adding to the token
			Cmt = 0

	#checking given input have any sting if have then add string in token[] list
	elif (i == '"') or (i == "'"):
		if Str:
			tokens.append(token) 
			token = ''
		Str = not Str

	elif Str:
		token = token + i

	
  #checking given input have any number or word if have then add this number and word in token[] list         
	elif i.isalnum() and not Word: # isalnum() is a built-in Python function that checks whether all characters in a string are alphanumeric.
		Word = True
		token = i

  #checking given input have any punctuation and parenthesis or at a time operator if have then added  in token[] list  
	elif (i in punctuation) or (i in parenthesis) or (i in operators):
		if token:
			tokens.append(token)
			token = ''
        
		if not (i == ' ' or i == '\n' or i == '	'):
			tokens.append(i)

	elif Word:
		token = token+i

tokens = list(set(tokens))

print("-------------")
print(tokens)
print("")

for token in tokens:


    if token in operators:
        op.append(token)

    elif token in keywords:
        key.append(token)

   

    elif re.search("^[_a-zA-Z][_a-zA-Z0-9]*$", token):
        identifier.append(token)

    elif token in punctuation:
        pun.append(token)

    elif token in parenthesis:
        par.append(token)

    else:
        constant.append(token)



print("\nNumber of keywords --> ",len(key), '---->', key)

print("\nNumber of identifiers-> ",len(identifier), '---->', identifier)

print("\nNumber of Arithmetic operators-> ",len(op), '---->', op)

print("\nNumber of constants = ",len(constant), '---->', constant)

print("\nNumber of Punctuation  = ",len(pun), '---->', pun)

print("\nNumber of Parenthesis  = ",len(par), '---->', par)
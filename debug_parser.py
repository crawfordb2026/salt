#!/usr/bin/env python3

from tokenizer import tokenize
from math_parser import Parser

with open('test_functions_edge_cases.salt', 'r') as f:
    lines = f.read().split('\n')

cleaned_lines = []
for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        cleaned_lines.append(line)

code = ' '.join(cleaned_lines)

print('Tokenizing...')
tokens = tokenize(code)
print('Tokens:', tokens)

print('\nParsing...')
parser = Parser(tokens)

statement_num = 1
while parser.current_token() is not None:
    print(f'\nStatement {statement_num}: Current token: {parser.current_token()}, Position: {parser.position}')
    try:
        ast = parser.parse()
        print(f'Parsed AST: {ast}')
        print(f'After parse - Current token: {parser.current_token()}, Position: {parser.position}')
    except Exception as e:
        print(f'Error: {e}')
        print(f'At token: {parser.current_token()}, Position: {parser.position}')
        # Show some context around the error
        start = max(0, parser.position - 5)
        end = min(len(tokens), parser.position + 5)
        print(f'Context: {tokens[start:end]}')
        break
    statement_num += 1
    # Skip stray closing braces at the top level
    while parser.current_token() == '}':
        print(f'Skipping closing brace at position {parser.position}')
        parser.advance() 
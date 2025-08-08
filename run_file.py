#!/usr/bin/env python3
"""
File Runner for Salt Programming Language

Usage: python3 run_file.py program.salt
"""

import sys
from tokenizer import tokenize
from math_parser import Parser
from interpreter import Interpreter


def run_file(filename):
    """Run a program file written in our language"""
    try:
        # Read the entire file
        with open(filename, 'r') as f:
            source_code = f.read()
        
        print(f"🚀 Running: {filename}")
        print("=" * 40)
        
        # Process the entire file as a stream of tokens
        # Remove comments and empty lines first
        cleaned_lines = []
        lines = source_code.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                cleaned_lines.append(line)
        
        # Join all lines and tokenize the entire content
        full_code = ' '.join(cleaned_lines)
        tokens = tokenize(full_code)
        
        interpreter = Interpreter()
        parser = Parser(tokens)
        
        # Parse and execute statements one by one
        statement_num = 1
        while parser.current_token() is not None:
            try:
                print(f"Statement {statement_num}:")
                
                # Parse one complete statement
                ast = parser.parse()
                if ast is None:
                    break  # No more statements to parse
                    
                result = interpreter.evaluate(ast)
                
                print(f"AST: {ast}")
                print(f"Result: {result}")
                print()
                
                statement_num += 1
                
            except Exception as e:
                print(f"❌ Error in statement {statement_num}: {e}")
                print(f"Current token: {parser.current_token()}")
                print(f"Position: {parser.position}/{len(tokens)}")
                break
    
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
    except Exception as e:
        print(f"❌ Error reading file: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 run_file.py <filename>")
        print("Example: python3 run_file.py program.salt")
        sys.exit(1)
    
    filename = sys.argv[1]
    run_file(filename)


if __name__ == "__main__":
    main() 
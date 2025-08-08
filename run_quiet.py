#!/usr/bin/env python3
"""
Quiet File Runner for Salt Programming Language

Usage: python3 run_quiet.py program.salt
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
        while parser.current_token() is not None:
            try:
                # Skip stray closing braces at the top level
                while parser.current_token() == '}':
                    parser.advance()
                
                if parser.current_token() is None:
                    break
                
                # Parse one complete statement
                ast = parser.parse()
                interpreter.evaluate(ast)
            except Exception as e:
                print(f"Error: {e}")
                break
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 run_quiet.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    run_file(filename)


if __name__ == "__main__":
    main() 
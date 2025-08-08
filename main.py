#!/usr/bin/env python3
"""
Simple Math Language - A basic calculator with proper order of operations

This demonstrates the three core components of a programming language:
1. Tokenizer (breaks text into tokens)
2. Parser (builds Abstract Syntax Tree with correct precedence) 
3. Interpreter (evaluates the tree to get results)
"""

from tokenizer import tokenize
from math_parser import Parser
from interpreter import Interpreter


def main():
    print("🧮 Simple Math Language Calculator")
    print("=" * 40)
    print("Enter math expressions like:")
    print("  3 + 5 * 2")
    print("  (10 + 5) / 3") 
    print("  2 * (3 + 4) - 1")
    print("\nType 'quit' or 'exit' to leave")
    print("Type 'debug' to see tokenization and parsing steps")
    print("-" * 40)
    
    interpreter = Interpreter()
    debug_mode = False
    
    while True:
        try:
            # Get user input
            user_input = input("\nmath> ").strip()
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if user_input.lower() == 'debug':
                debug_mode = not debug_mode
                status = "ON" if debug_mode else "OFF"
                print(f"Debug mode: {status}")
                continue
            
            if not user_input:
                continue
            
            # Process the expression through our language pipeline
            if debug_mode:
                print(f"\n🔍 Debug Info for: {user_input}")
                
                # Step 1: Tokenize
                tokens = tokenize(user_input)
                print(f"1. Tokens: {tokens}")
                
                # Step 2: Parse  
                parser = Parser(tokens)
                ast = parser.parse()
                print(f"2. AST: {ast}")
                
                # Step 3: Evaluate
                result = interpreter.evaluate(ast)
                print(f"3. Result: {result}")
            else:
                # Normal mode - just show the result
                tokens = tokenize(user_input)
                parser = Parser(tokens)
                ast = parser.parse()
                result = interpreter.evaluate(ast)
                print(f"= {result}")
                
        except ZeroDivisionError as e:
            print(f"❌ Math Error: {e}")
        except ValueError as e:
            print(f"❌ Syntax Error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")


def run_examples():
    """Show some example calculations"""
    print("\n🎯 Example Calculations:")
    print("-" * 25)
    
    examples = [
        "2 + 3",
        "5 * 4 - 2", 
        "10 / (2 + 3)",
        "(1 + 2) * (3 + 4)",
        "20 - 15 / 3 + 2"
    ]
    
    interpreter = Interpreter()
    
    for expr in examples:
        try:
            tokens = tokenize(expr)
            parser = Parser(tokens)
            ast = parser.parse()
            result = interpreter.evaluate(ast)
            print(f"{expr:20} = {result}")
        except Exception as e:
            print(f"{expr:20} = Error: {e}")


if __name__ == "__main__":
    # Show examples first
    run_examples()
    
    # Then start interactive mode
    main()

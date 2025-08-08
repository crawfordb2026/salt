# Salt Programming Language

A basic programming language that can evaluate mathematical expressions with proper order of operations.

## 🚀 Quick Start

### Run a program file:
```bash
./salt example.salt
```

### Interactive calculator:
```bash
python3 main.py
```

## 📁 File Structure

- `tokenizer.py` - Breaks source code into tokens
- `math_parser.py` - Builds Abstract Syntax Tree with correct precedence  
- `interpreter.py` - Evaluates the AST to get results
- `run_file.py` - Runs .salt program files
- `salt` - Executable script (like `python` command)
- `main.py` - Interactive REPL calculator
- `example.salt` - Example program in Salt

## 🧮 Language Features

### Supported Operations:
- Addition: `3 + 5`
- Subtraction: `10 - 3`
- Multiplication: `4 * 6`
- Division: `20 / 4`
- Parentheses: `(2 + 3) * 4`
- Decimal numbers: `3.14 * 2`

### Order of Operations:
- Multiplication and division before addition and subtraction
- Parentheses override default order
- Left-to-right evaluation for same precedence

## 📝 Writing Programs

Create a `.salt` file with your math expressions:

```salt
# This is a comment
3 + 5
(10 + 20) / 6
2.5 * 4
```

Then run it:
```bash
./salt myprogram.salt
```

## 🛠 Architecture

This language demonstrates the three core components of any programming language:

1. **Lexer/Tokenizer** (`tokenizer.py`)
   - Converts source code into tokens
   - Handles numbers, operators, parentheses

2. **Parser** (`math_parser.py`) 
   - Builds Abstract Syntax Tree (AST)
   - Handles operator precedence
   - Manages parentheses grouping

3. **Interpreter** (`interpreter.py`)
   - Walks the AST tree
   - Evaluates expressions recursively
   - Returns final results

## 🎯 Examples

```salt
# Basic math
2 + 3           # = 5

# Order of operations
2 + 3 * 4       # = 14 (not 20)

# Parentheses
(2 + 3) * 4     # = 20

# Complex expressions
((5 + 3) * 2) - 6    # = 10
``` 
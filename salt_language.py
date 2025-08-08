"""
This file contains all core Salt language keywords, types, operators, and statement starters.
If you add a new keyword, type, or operator to Salt, update this file!
"""

KEYWORDS = {
    'make', 'int', 'string', 'bool', 'TRUE', 'FALSE', 'double', 'not', 'and', 'or',
    'eq', 'neq', 'gt', 'lt', 'gteq', 'lteq', 'print', 'if', 'loop', 'while', 'from',
    'to', 'by', 'skip', 'end', 'function', 'takes', 'gives', 'give', 'array'
}

TYPES = {'int', 'string', 'bool', 'double'}

OPERATORS = {'+', '-', '*', '/', '%', '(', ')', '<', '>', '=', '!', '{', '}', ',','[',']'}

STATEMENT_STARTERS = {
    'make', 'print', 'if', 'loop', 'while', 'skip', 'end', 'give'
} 
from salt_language import KEYWORDS, OPERATORS

def tokenize(text):
    """
    Tokenizes a Salt expression into a list of tokens.
    Handles numbers, operators, parentheses, identifiers, make keyword, and types.
    """
    tokens = []
    i = 0
    
    while i < len(text):
        char = text[i]
        
        # Skip whitespace
        if char.isspace():
            i += 1
            continue
        
        # Handle comments (skip everything from # to end of line)
        if char == '#':
            while i < len(text) and text[i] != '\n':
                i += 1
            continue
        
        # Handle numbers (including decimals)
        if char.isdigit():
            number = ''
            while i < len(text) and (text[i].isdigit() or text[i] == '.'):
                number += text[i]
                i += 1
            tokens.append(number)
            continue
        
        # Handle string literals
        if char == '"':
            string_value = ''
            i += 1  # Skip opening quote
            while i < len(text) and text[i] != '"':
                string_value += text[i]
                i += 1
            if i < len(text):  # Skip closing quote
                i += 1
            tokens.append(f'"{string_value}"')
            continue
        
        # Handle identifiers, keywords, and variable names
        if char.isalpha() or char == '_':
            identifier = ''
            while i < len(text) and (text[i].isalnum() or text[i] == '_'):
                identifier += text[i]
                i += 1
            tokens.append(identifier)
            continue
        
        # Handle operators, parentheses, braces, and comma
        if char in OPERATORS:
            tokens.append(char)
            i += 1
            continue
        
        # Skip unknown characters for now
        i += 1
    
    return tokens


def test_tokenizer():
    """Test the tokenizer with Salt syntax examples"""
    test_cases = [
        "make int x 5",
        "make string name \"hello\"",
        "make bool flag TRUE",
        "x + 10",
        "make int result x * 2",
        "make double result x * 2.2"
    ]
    
    print("Testing Salt tokenizer:")
    for test in test_cases:
        tokens = tokenize(test)
        print(f"'{test}' -> {tokens}")


if __name__ == "__main__":
    test_tokenizer()



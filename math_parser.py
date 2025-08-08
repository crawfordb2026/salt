from tokenizer import tokenize
from salt_language import KEYWORDS, TYPES, STATEMENT_STARTERS

class ASTNode:
    """Base class for all AST nodes"""
    pass

class NumberNode(ASTNode):
    """Represents a number in the AST"""
    def __init__(self, value):
        # Preserve integer vs float based on whether there's a decimal point
        if '.' in str(value):
            self.value = float(value)
        else:
            self.value = int(value)
    
    def __repr__(self):
        return f"Number({self.value})"

class StringNode(ASTNode):
    """Represents a string in the AST"""
    def __init__(self, value):
        self.value = value  # Keep quotes for now
    
    def __repr__(self):
        return f"String({self.value})"

class BooleanNode(ASTNode):
    """Represents a boolean in the AST"""
    def __init__(self, value):
        self.value = value == 'TRUE'
    
    def __repr__(self):
        return f"Boolean({self.value})"

class VariableNode(ASTNode):
    """Represents a variable reference in the AST"""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Variable({self.name})"


class AssignmentNode(ASTNode):
    """changes the value of an existing varaible: make name value"""
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value
    
    def __repr__(self):
        return f"Make({self.var_name} = {self.value})"

class DeclarationNode(ASTNode):
    """Represents a variable declaration in Salt: make type name value"""
    def __init__(self, var_type, var_name, value):
        self.var_type = var_type
        self.var_name = var_name
        self.value = value
    
    def __repr__(self):
        return f"Make({self.var_type} {self.var_name} = {self.value})"

class BinaryOpNode(ASTNode):
    """Represents a binary operation (+, -, *, /) in the AST"""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"BinOp({self.left} {self.operator} {self.right})"

class LogicalNode(ASTNode): 
    """for parsing 'and' and 'or' and 'not'"""
    def __init__(self, left, operator, right=None):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self):
        if self.right:
            return f"Logical({self.left} {self.operator} {self.right})"
        else: 
            return f"Logical({self.operator} {self.left})"
            

class ComparisonNode(ASTNode):
    """for parsing comparisons like x gt 5"""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self):
        return f"Comparison({self.left} {self.operator} {self.right})"

class IfNode(ASTNode): 
    """for parsing if statements"""
    def __init__(self, condition, code_block):
        self.condition = condition
        self.code_block = code_block  # List of statements in the block
    
    def __repr__(self):
        return f"If({self.condition}, {self.code_block})"
    
class ForNode(ASTNode):
    def __init__(self, var, code_block, startIndex=None, endIndex=None, step=None):
        self.var = var
        self.code_block = code_block 
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.step = step

    def __repr__(self):
        if self.startIndex is None:
            return f"For({self.var} times, {self.code_block})"
        else:
            return f"For({self.var} from {self.startIndex} to {self.endIndex}, {self.code_block})"

class WhileNode(ASTNode):
    def __init__(self, condition, code_block):
        self.condition = condition
        self.code_block = code_block 
    def __repr__(self):
        return f"While({self.condition}, {self.code_block})"
    
class SkipNode(ASTNode):
    """Represents a skip statement (continue)"""
    def __repr__(self):
        return "Skip()"

class EndNode(ASTNode):
    """Represents an end statement (break)"""
    def __repr__(self):
        return "End()"
    
class ArrayNode(ASTNode):
    """Represents an array declaration or array element assignment"""
    def __init__(self, var_type=None, var_name=None, size=None, index=None, value=None, is_declaration=True):
        self.var_type = var_type  # For declarations
        self.var_name = var_name
        self.size = size  # For declarations
        self.index = index  # For assignments/access
        self.value = value  # For assignments
        self.is_declaration = is_declaration  # True for declarations, False for assignments
    
    def __repr__(self):
        if self.is_declaration:
            return f"ArrayDecl({self.var_type} {self.var_name}[{self.size}])"
        else:
            return f"ArrayAssign({self.var_name}[{self.index}] = {self.value})"


class PrintNode(ASTNode):
    """Represents a print statement: print expression1 expression2 ..."""
    def __init__(self, expressions):
        self.expressions = expressions  # List of expressions to print
    
    def __repr__(self):
        return f"Print({self.expressions})"

class FunctionNode(ASTNode):
    """Represents a function definition"""
    def __init__(self, name, return_type, parameters, code_block):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters  # List of (type, name) tuples
        self.code_block = code_block
    
    def __repr__(self):
        return f"Function({self.name}, {self.return_type}, {self.parameters}, {self.code_block})"

class FunctionCallNode(ASTNode):
    """Represents a function call"""
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments  # List of expressions
    
    def __repr__(self):
        return f"FunctionCall({self.name}, {self.arguments})"

class ReturnNode(ASTNode):
    """Represents a return statement"""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Return({self.value})"

class UnaryOpNode(ASTNode):
    """Represents a unary operation (e.g., -x) in the AST"""
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
    def __repr__(self):
        return f"UnaryOp({self.operator}{self.operand})"

class ArrayAccessNode(ASTNode):
    """Represents array element access: array_name[index]"""
    def __init__(self, array_name, index):
        self.array_name = array_name
        self.index = index
    
    def __repr__(self):
        return f"ArrayAccess({self.array_name}[{self.index}])"

class Parser:
    """Parses tokens into an Abstract Syntax Tree"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self):
        """Get the current token without advancing"""
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]
    
    def advance(self):
        """Move to the next token"""
        self.position += 1
    
    def parse_primary(self):
        """Parse a number, variable, string, boolean, unary minus, or parenthesized expression"""
        token = self.current_token()
        
        if token is None:
            raise ValueError("Unexpected end of input")
        
        if token == '-':
            self.advance()
            operand = self.parse_primary()
            return UnaryOpNode('-', operand)
        
        if token.replace('.', '').isdigit():
            # It's a number
            self.advance()
            return NumberNode(token)
        elif token.startswith('"') and token.endswith('"'):
            # It's a string
            self.advance()
            return StringNode(token)
        elif token == 'TRUE' or token == 'FALSE':
            self.advance()
            return BooleanNode(token)
        elif token == '(':  # Parenthesized expression
            self.advance()
            expr = self.parse_comparison()
            if self.current_token() != ')':
                raise ValueError(f"Expected ')', got {self.current_token()}")
            self.advance()
            return expr
        elif (token[0].isalpha() or token[0] == '_') and all(c.isalnum() or c == '_' for c in token) and token not in KEYWORDS:
            # It's a variable or function call
            name = token
            self.advance()
            
            # Check for array access: variable_name[index]
            if self.current_token() == '[':
                self.advance()  # Skip '['
                index = self.parse_comparison()  # Parse the index expression
                if self.current_token() != ']':
                    raise ValueError(f"Expected ']', got {self.current_token()}")
                self.advance()  # Skip ']'
                return ArrayAccessNode(name, index)
            elif self.current_token() == '(':  # Function call
                return self.parse_function_call(name)
            else:
                return VariableNode(name)
        else:
            raise ValueError(f"Expected number, variable, string, boolean, or '(', got {token}")
    
    def parse_term(self):
        """Parse multiplication, division, and modulo (higher precedence)"""
        result = self.parse_primary()
        
        while self.current_token() in ['*', '/', '%']:
            operator = self.current_token()
            self.advance()
            right = self.parse_primary()
            result = BinaryOpNode(result, operator, right)
        
        return result
    
    def parse_expression(self):
        """Parse addition and subtraction (lower precedence)"""
        result = self.parse_term()
        
        while self.current_token() in ['+', '-']:
            operator = self.current_token()
            self.advance()
            right = self.parse_term()
            result = BinaryOpNode(result, operator, right)
        
        return result
    
    def parse_comparison(self):
        """parses comparisons and logical arguments"""
        if self.current_token() == 'not': 
            self.advance()
            operand = self.parse_expression()
            return LogicalNode(operand, 'not', None)
        
        left = self.parse_expression() # get left and move on

        operator = self.current_token() #get the middle and check later
    
        if operator in ['and', 'or']: #NOW check what operator it is
            self.advance()
            right = self.parse_expression()
            return LogicalNode(left, operator, right)
        elif operator in ['lt', 'gt', 'lteq', 'gteq', 'eq', 'neq']:
            self.advance()
            right = self.parse_expression()
            return ComparisonNode(left, operator, right)
        
        # If no operator found, just return the left expression
        return left

    def parse_if_statement(self):
        """parse if statement with condition and code block, and optional else block"""
        self.advance()  # skip the 'if'
        
        # Parse the condition
        condition = self.parse_comparison()
        
        # Expect '{'
        if self.current_token() != '{':
            raise ValueError(f"Expected '{{' after if condition, got {self.current_token()}")
        self.advance()  # skip '{'
        
        # Parse code block - collect statements until we hit '}'
        code_block = []
        while self.current_token() != '}':
            if self.current_token() is None:
                raise ValueError("Expected '}' to close if block, reached end of input")
            # Parse each statement in the block
            statement = self.parse_statement()
            if statement is not None:  # Only add non-None statements
                code_block.append(statement)
        
        # Skip the closing '}'
        self.advance()
        
        # Check for optional else block
        else_block = None
        if self.current_token() == 'else':
            self.advance()  # skip 'else'
            if self.current_token() != '{':
                raise ValueError(f"Expected '{{' after else, got {self.current_token()}")
            self.advance()  # skip '{'
            else_block = []
            while self.current_token() != '}':
                if self.current_token() is None:
                    raise ValueError("Expected '}' to close else block, reached end of input")
                statement = self.parse_statement()
                if statement is not None:
                    else_block.append(statement)
            self.advance()  # skip closing '}'
        
        return IfNode(condition, code_block if else_block is None else (code_block, else_block))

    def parse_make_statement(self):
        """Parse a make statement - make type name value or make name[index] value"""
        self.advance()  # Skip 'make'
        token2 = self.current_token()
        
        # Check if this is a function definition
        if token2 == 'function': 
            return self.parse_function_definition()
        
        # Check if this is an array declaration: make int array name[size]
        if token2 in TYPES:
            var_type = token2
            self.advance()
            
            # Check for 'array' keyword
            if self.current_token() == 'array':
                self.advance()  # Skip 'array'
                
                # Get array name
                var_name = self.current_token()
                if not var_name or not (var_name[0].isalpha() or var_name[0] == '_') or not all(c.isalnum() or c == '_' for c in var_name) or var_name in KEYWORDS:
                    raise ValueError(f"Expected array name, got {var_name}")
                self.advance()
                
                # Expect '['
                if self.current_token() != '[':
                    raise ValueError(f"Expected '[', got {self.current_token()}")
                self.advance()
                
                # Parse array size
                size = self.parse_comparison()
                
                # Expect ']'
                if self.current_token() != ']':
                    raise ValueError(f"Expected ']', got {self.current_token()}")
                self.advance()
                
                return ArrayNode(var_type=var_type, var_name=var_name, size=size, is_declaration=True)
            else:
                # Regular variable declaration: make type name value
                var_name = self.current_token()
                if not var_name or not (var_name[0].isalpha() or var_name[0] == '_') or not all(c.isalnum() or c == '_' for c in var_name) or var_name in KEYWORDS:
                    raise ValueError(f"Expected variable name, got {var_name}")
                self.advance()
                
                value = self.parse_comparison()
                return DeclarationNode(var_type, var_name, value)
        
        else:
            # This is an assignment: make name value or make name[index] value
            var_name = self.current_token()
            if not var_name or not (var_name[0].isalpha() or var_name[0] == '_') or not all(c.isalnum() or c == '_' for c in var_name) or var_name in KEYWORDS:
                raise ValueError(f"Expected variable name, got {var_name}")
            self.advance()
            
            # Check if this is an array element assignment: make name[index] value
            if self.current_token() == '[':
                self.advance()  # Skip '['
                index = self.parse_comparison()
                
                if self.current_token() != ']':
                    raise ValueError(f"Expected ']', got {self.current_token()}")
                self.advance()
                
                value = self.parse_comparison()
                return ArrayNode(var_name=var_name, index=index, value=value, is_declaration=False)
            else:
                # Regular assignment: make name value
                value = self.parse_comparison()
                return AssignmentNode(var_name, value)
    
    def parse_function_definition(self):
        """Parse a function definition: make function name takes params gives return_type"""
        self.advance()  # Skip 'function'
        
        # Get function name
        func_name = self.current_token()
        if not func_name or not (func_name[0].isalpha() or func_name[0] == '_') or not all(c.isalnum() or c == '_' for c in func_name) or func_name in KEYWORDS:
            raise ValueError(f"Expected function name, got {func_name}")
        self.advance()
        
        # Check if function has parameters or not
        if self.current_token() == 'gives':
            # Function with no parameters
            parameters = []
            self.advance()  # Skip 'gives'
        elif self.current_token() == 'takes':
            # Function with parameters
            self.advance()  # Skip 'takes'
            parameters = []
            while True:
                # Parse parameter type
                param_type = self.current_token()
                if param_type not in TYPES:
                    raise ValueError(f"Expected parameter type, got {param_type}")
                self.advance()
                # Parse parameter name
                param_name = self.current_token()
                if not param_name or not (param_name[0].isalpha() or param_name[0] == '_') or not all(c.isalnum() or c == '_' for c in param_name) or param_name in KEYWORDS:
                    raise ValueError(f"Expected parameter name, got {param_name}")
                self.advance()
                parameters.append((param_type, param_name))
                # Check for comma or 'gives'
                if self.current_token() == ',':
                    self.advance()  # Skip comma and continue to next parameter
                    continue
                elif self.current_token() == 'gives':
                    break
                else:
                    raise ValueError(f"Expected ',' or 'gives', got {self.current_token()}")
            self.advance()  # Skip 'gives'
        else:
            raise ValueError(f"Expected 'takes' or 'gives' after function name, got {self.current_token()}")
        # Parse return type
        return_type = self.current_token()
        if return_type not in TYPES:
            raise ValueError(f"Expected return type, got {return_type}")
        self.advance()  # Skip return type
        # Expect '{'
        if self.current_token() != '{':
            raise ValueError(f"Expected '{{' after function signature, got {self.current_token()}")
        self.advance()
        
        # Parse function body
        code_block = []
        while self.current_token() != '}':
            if self.current_token() is None:
                raise ValueError("Expected '}' to close function block, reached end of input")
            statement = self.parse_statement()
            if statement is not None:
                code_block.append(statement)
        
        # Skip closing '}'
        self.advance()
        
        return FunctionNode(func_name, return_type, parameters, code_block)

    def is_statement_starter(self, token):
        """Check if a token starts a new statement"""
        return token in STATEMENT_STARTERS
    
    def parse_print_statement(self):
        """Parse a print statement: print expression1 expression2 ..."""
        self.advance()  # Skip 'print'
        expressions = []
        
        # Keep parsing expressions until we hit a new statement or end of block
        while self.current_token() is not None and not self.is_statement_starter(self.current_token()) and self.current_token() != '}':
            expression = self.parse_comparison()
            expressions.append(expression)
        
        return PrintNode(expressions)
    
    def parse_loop_statement(self):
        """parse thru loop statement which is a for loop in python"""
        self.advance() # skip 'loop'
        
        # Check if it's a literal number or a variable name
        token = self.current_token()
        if token and token.replace('.', '').isdigit():
            # It's a literal number like "loop 5 times"
            var = int(token)
            self.advance()
            if self.current_token() == 'times':
                self.advance()
                # For simple "loop 5 times", use None values
                startIndex = None
                endIndex = None
                step = None
            else:
                raise ValueError(f"Expected 'times' after number, got {self.current_token()}")
        elif token and (token[0].isalpha() or token[0] == '_') and all(c.isalnum() or c == '_' for c in token) and token not in KEYWORDS:
            # It's a variable name like "loop x from 1 to 10"
            var = token  # Store variable name as string
            self.advance()
            if self.current_token() == 'from':
                self.advance()
                if self.current_token() and self.current_token().replace('.', '').isdigit():
                    startIndex = int(self.current_token())
                    self.advance()
                    if self.current_token() != 'to':
                        raise ValueError(f"Expected 'to' after start index, got {self.current_token()}")
                    self.advance()
                    if self.current_token() and self.current_token().replace('.', '').isdigit():
                        endIndex = int(self.current_token())
                        self.advance()
                        step = 1  # Default step (not really neccesary)
                        if self.current_token() == 'by':
                            self.advance()
                            if self.current_token() and self.current_token().replace('.', '').isdigit():
                                step = int(self.current_token())
                                self.advance()
                            else:
                                raise ValueError(f"Expected number after 'by', got {self.current_token()}")
                    else:
                        raise ValueError(f"Expected number after 'to', got {self.current_token()}")
                else:
                    raise ValueError(f"Expected number after 'from', got {self.current_token()}")
            else:
                raise ValueError(f"Expected 'from' after variable name, got {self.current_token()}")
        else: 
            raise ValueError(f"Expected number or variable name after 'loop', got {token}")

        if self.current_token() != '{':
            raise ValueError(f"Expected '{{' after loop condition, got {self.current_token()}")
        self.advance()  # skip '{'
        
        code_block = []
        while self.current_token() != '}':
            if self.current_token() is None:
                raise ValueError("Expected '}' to close loop block, reached end of input")
            # Parse each statement in the block
            statement = self.parse_statement()
            if statement is not None:  # Only add non-None statements
                code_block.append(statement)
        # skip the closing '}'
        self.advance() 
        return ForNode(var, code_block, startIndex, endIndex, step)
    
    def parse_while_statement(self):
        """parse thru while statement"""
        self.advance() # skip 'while'
        
        condition = self.parse_comparison()
        
        if self.current_token() != '{':
            raise ValueError(f"Expected '{{' after while condition, got {self.current_token()}")
        self.advance()  # skip '{'
        
        code_block = []
        while self.current_token() != '}':
            if self.current_token() is None:
                raise ValueError("Expected '}' to close while block, reached end of input")
            # Parse each statement in the block
            statement = self.parse_statement()
            if statement is not None:  # Only add non-None statements
                code_block.append(statement)
        # skip the closing '}'
        self.advance() 
        return WhileNode(condition, code_block)

    def parse_statement(self):
        """Parse a statement (make declaration, print statement, or expression)"""
        token = self.current_token()
        if token is None:
            return None
        elif token == 'make':
            return self.parse_make_statement()
        elif token == 'print':
            return self.parse_print_statement()
        elif token == 'skip':
            self.advance()  # Advance past 'skip'
            return SkipNode()
        elif token == 'end':
            self.advance()  # Advance past 'end'
            return EndNode()
        elif token == 'give':
            return self.parse_give_statement()
        elif token == 'if':
            return self.parse_if_statement()
        elif token == 'loop':
            return self.parse_loop_statement()
        elif token == 'while':
            return self.parse_while_statement()
        elif token == '}':  # Don't try to parse the closing brace as a statement
            return None
        else:
            return self.parse_comparison()
    
    def parse_give_statement(self):
        """Parse a give statement (return statement)"""
        self.advance()  # Skip 'give'
        
        # Parse the return value
        value = self.parse_comparison()
        
        return ReturnNode(value)
    
    def parse_function_call(self, func_name):
        """Parse a function call: name(arg1, arg2, ...)"""
        self.advance()  # Skip '('
        
        arguments = []
        
        # Parse arguments until we hit ')'
        while self.current_token() != ')':
            if self.current_token() is None:
                raise ValueError("Expected ')' to close function call, reached end of input")
            
            # Parse argument expression
            arg = self.parse_comparison()
            arguments.append(arg)
            
            # Check for comma or closing parenthesis
            if self.current_token() == ',':
                self.advance()
            elif self.current_token() != ')':
                raise ValueError(f"Expected ',' or ')', got {self.current_token()}")
        
        # Skip closing ')'
        self.advance()
        
        return FunctionCallNode(func_name, arguments)
    
    def parse(self):
        """Parse the entire statement"""
        return self.parse_statement()
    
#end of parser class

def print_tree(node, indent=0):
    """Pretty print the AST tree"""
    spaces = "  " * indent
    
    if isinstance(node, NumberNode):
        print(f"{spaces}Number: {node.value}")
    elif isinstance(node, StringNode):
        print(f"{spaces}String: {node.value}")
    elif isinstance(node, BooleanNode):
        print(f"{spaces}Boolean: {node.value}")
    elif isinstance(node, VariableNode):
        print(f"{spaces}Variable: {node.name}")
    elif isinstance(node, DeclarationNode):
        print(f"{spaces}Declaration {node.var_type} {node.var_name} =")
        print_tree(node.value, indent + 1)
    elif isinstance(node, AssignmentNode):
        print(f"{spaces}Assignment {node.var_name} =")
        print_tree(node.value, indent + 1)
    elif isinstance(node, BinaryOpNode):
        print(f"{spaces}{node.operator}")
        print_tree(node.left, indent + 1)
        print_tree(node.right, indent + 1)
    elif isinstance(node, ComparisonNode):
        print(f"{spaces}Comparison{node.left}{node.operator}{node.right}")
    elif isinstance(node, LogicalNode):
        if node.right:
            print(f"{spaces}Logical{node.left}{node.operator}{node.right}")
        else:
            print(f"{spaces}Comparison{node.operator}{node.left}")
    elif isinstance(node, UnaryOpNode):
        print(f"{spaces}UnaryOp({node.operator}{node.operand})")



def test_parser():
    """Test the parser with Salt syntax"""
    test_cases = [
        "make int x 5",
        "make string name \"hello\"",
        "make bool flag TRUE",
        "x + 10",
        "make int result x * 2"
    ]
    
    print("Testing Salt parser:")
    print("=" * 40)
    
    for expression in test_cases:
        print(f"\nExpression: {expression}")
        tokens = tokenize(expression)
        print(f"Tokens: {tokens}")
        
        try:
            parser = Parser(tokens)
            ast = parser.parse()
            print(f"AST: {ast}")
            print("Tree structure:")
            print_tree(ast)
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 20)


if __name__ == "__main__":
    test_parser() 
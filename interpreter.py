from math_parser import Parser, NumberNode, StringNode, BooleanNode, VariableNode, AssignmentNode, DeclarationNode, BinaryOpNode, ComparisonNode, LogicalNode, PrintNode, IfNode, ForNode, WhileNode, SkipNode, EndNode, FunctionNode, FunctionCallNode, ReturnNode, UnaryOpNode, ArrayNode, ArrayAccessNode
from tokenizer import tokenize
from salt_language import TYPES


class Interpreter:
    """Evaluates Abstract Syntax Trees for Salt language"""
    
    def __init__(self):
        self.variables = {}  # Store variable values
        self.functions = {}  # Store function definitions
        self.SKIP = object()
        self.END = object()
    def evaluate(self, node):
        """Recursively evaluate an AST node"""
        
        if isinstance(node, NumberNode):
            return node.value
        
        elif isinstance(node, StringNode):
            # Remove quotes from string
            return node.value.strip('"')
        
        elif isinstance(node, BooleanNode):
            return node.value
        
        elif isinstance(node, VariableNode):
            if node.name in self.variables:
                return self.variables[node.name]['value']
            else:
                raise NameError(f"Variable '{node.name}' is not defined")
        
        elif isinstance(node, DeclarationNode):
            # Evaluate the value and store it
            if node.var_name in self.variables:
                raise NameError(f"Variable '{node.var_name}' already defined")

            value = self.evaluate(node.value)
            # disinguish between int and doubles, ints will be truncated
            if node.var_type == 'int':
                value = int(value)
            elif node.var_type == 'double':
                value = float(value)    
            elif node.var_type == 'bool':
                value = bool(value)
            elif node.var_type == 'string':
                value = str(value)
            else: 
                raise ValueError(f"Unknown variable type: {node.var_type}")

            self.variables[node.var_name] = {'value': value, 'type': node.var_type}
            # print(f"Made {node.var_type} {node.var_name} = {value}")
            return value
        
        elif isinstance(node, AssignmentNode):
            # Evaluate the value and store it
            if node.var_name not in self.variables:
                raise NameError(f"Variable '{node.var_name}' is not defined")
            
            value = self.evaluate(node.value)

            if self.variables[node.var_name]['type'] == 'int':
                value = int(value)
            elif self.variables[node.var_name]['type'] == 'double':
                value = float(value)
            elif self.variables[node.var_name]['type'] == 'bool':
                value = bool(value)
            elif self.variables[node.var_name]['type'] == 'string':
                value = str(value)
                

            self.variables[node.var_name]['value'] = value
            # print(f"Made {node.var_name} = {value}")
            return value
        
        elif isinstance(node, BinaryOpNode):
            # Evaluate left and right sides first
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            
            # Apply the operator
            if node.operator == '+':
                # If either operand is a string, concatenate as strings
                if isinstance(left_val, str) or isinstance(right_val, str):
                    return str(left_val) + str(right_val)
                return left_val + right_val
            elif node.operator == '-':
                return left_val - right_val
            elif node.operator == '*':
                return left_val * right_val
            elif node.operator == '/':
                if right_val == 0:
                    raise ZeroDivisionError("Cannot divide by zero!")
                return left_val / right_val
            elif node.operator == '%':
                if right_val == 0:
                    raise ZeroDivisionError("Cannot modulo by zero!")
                return left_val % right_val
            else:
                raise ValueError(f"Unknown operator: {node.operator}")
            
        elif isinstance(node, LogicalNode):
            if (node.right):
                leftVal = self.evaluate(node.left)
                rightVal = self.evaluate(node.right)

                if node.operator == 'and':
                    return leftVal and rightVal
                elif node.operator == 'or':
                    return leftVal or rightVal
                else:
                    raise ValueError(f"Unknown logical operator: {node.operator}")
                    
            else:
                leftVal = self.evaluate(node.left)  

                if node.operator == 'not':
                    return not leftVal  
                else:
                    raise ValueError(f"Unknown logical operator: {node.operator}")

        elif isinstance(node, ComparisonNode):
            leftVal = self.evaluate(node.left)
            rightVal = self.evaluate(node.right)

            if node.operator == 'eq': 
                return leftVal == rightVal
            elif node.operator == 'neq': 
                return leftVal != rightVal
            elif node.operator == 'lt':   
                return leftVal < rightVal
            elif node.operator == 'gt': 
                return leftVal > rightVal
            elif node.operator == 'lteq': 
                return leftVal <= rightVal
            elif node.operator == 'gteq': 
                return leftVal >= rightVal
            else:
                raise ValueError(f"Unknown comparison operator: {node.operator}")
        
        elif isinstance(node, IfNode):
            # Evaluate the condition
            condition_result = self.evaluate(node.condition)
            
            # IfNode.code_block can be a list (if only if-block) or a tuple (if-block, else-block)
            if isinstance(node.code_block, tuple):
                if_block, else_block = node.code_block
            else:
                if_block = node.code_block
                else_block = None
            
            if condition_result:
                result = None
                for statement in if_block:
                    result = self.evaluate(statement)
                    # Check for SKIP or END and propagate them up
                    if result is self.SKIP or result is self.END:
                        return result
                return result
            else:
                if else_block is not None:
                    result = None
                    for statement in else_block:
                        result = self.evaluate(statement)
                        if result is self.SKIP or result is self.END:
                            return result
                    return result
                return None  # If condition is false and no else block, do nothing
        
        elif isinstance(node, PrintNode):
            # Evaluate all expressions and concatenate them
            values = []
            for expr in node.expressions:
                value = self.evaluate(expr)
                values.append(str(value))
            
            # Join all values and print
            result = ''.join(values)
            print(result)
            return result  # Return the printed value
        
        elif isinstance(node, ArrayNode):
            if node.is_declaration:
                # Array declaration: make int array name[size]
                if node.var_name in self.variables:
                    raise NameError(f"Variable '{node.var_name}' already defined")
                
                size = self.evaluate(node.size)
                if not isinstance(size, int) or size <= 0:
                    raise ValueError(f"Array size must be a positive integer, got {size}")
                
                # Initialize array with default values based on type
                if node.var_type == 'int':
                    array_data = [0] * size
                elif node.var_type == 'double':
                    array_data = [0.0] * size
                elif node.var_type == 'string':
                    array_data = [""] * size
                elif node.var_type == 'bool':
                    array_data = [False] * size
                else:
                    raise ValueError(f"Unknown array type: {node.var_type}")
                
                self.variables[node.var_name] = {
                    'value': array_data, 
                    'type': f'array_{node.var_type}',
                    'element_type': node.var_type,
                    'size': size
                }
                return array_data
            else:
                # Array element assignment: make name[index] value
                if node.var_name not in self.variables:
                    raise NameError(f"Array '{node.var_name}' is not defined")
                
                var_info = self.variables[node.var_name]
                if not var_info['type'].startswith('array_'):
                    raise TypeError(f"'{node.var_name}' is not an array")
                
                index = self.evaluate(node.index)
                if not isinstance(index, int) or index < 0 or index >= var_info['size']:
                    raise IndexError(f"Array index {index} out of bounds for array '{node.var_name}' of size {var_info['size']}")
                
                value = self.evaluate(node.value)
                
                # Type conversion based on array element type
                element_type = var_info['element_type']
                if element_type == 'int':
                    value = int(value)
                elif element_type == 'double':
                    value = float(value)
                elif element_type == 'bool':
                    value = bool(value)
                elif element_type == 'string':
                    value = str(value)
                
                var_info['value'][index] = value
                return value
        
        elif isinstance(node, ArrayAccessNode):
            # Array element access: name[index]
            if node.array_name not in self.variables:
                raise NameError(f"Array '{node.array_name}' is not defined")
            
            var_info = self.variables[node.array_name]
            if not var_info['type'].startswith('array_'):
                raise TypeError(f"'{node.array_name}' is not an array")
            
            index = self.evaluate(node.index)
            if not isinstance(index, int) or index < 0 or index >= var_info['size']:
                raise IndexError(f"Array index {index} out of bounds for array '{node.array_name}' of size {var_info['size']}")
            
            return var_info['value'][index]
        
        elif isinstance(node, ForNode):
            #evaluate the for node
            if node.startIndex is None:  # Check explicitly for None
                for i in range(node.var):
                    
                    for statement in node.code_block:
                        result = self.evaluate(statement)
                        if result is self.SKIP:
                            break  # Break out of inner loop (statements)
                        elif result is self.END:
                            return None  # Break out of outer loop (for loop)
                return None
            else:
                # Variable-based loops like "loop i from 1 to 10"
                if node.var in self.variables:
                    if self.variables[node.var]['type'] == 'int':
                        for i in range(node.startIndex, node.endIndex+1, node.step):
                            # Update the loop variable to current iteration value
                            self.variables[node.var]['value'] = i
                            for statement in node.code_block:
                                result = self.evaluate(statement)
                                if result is self.SKIP:
                                    break  # Break out of inner loop (statements)
                                elif result is self.END:
                                    return None  # Break out of outer loop (for loop)
                        return None
                    else:
                        raise ValueError(f"Variable {node.var} is not an integer")
                else:
                    raise ValueError(f"Loop variable '{node.var}' is not defined")

        elif isinstance(node, WhileNode):
            # evaluate the condition of the loop
            condition_result = self.evaluate(node.condition)

            while condition_result:
                #reevaluate condition each tijme

                for statement in node.code_block:
                    result = self.evaluate(statement)
                    if result is self.SKIP:
                        break  # Break out of inner loop (statements)
                    elif result is self.END:
                        return None  # Break out of outer loop (while loop)
                condition_result = self.evaluate(node.condition)
            return None 
        
        elif isinstance(node, SkipNode):
            return self.SKIP
        elif isinstance(node, EndNode):
            return self.END
        elif isinstance(node, FunctionNode):
            # Store function definition in a functions dictionary
            self.functions[node.name] = node
            return None  # Function definitions don't return a value
        elif isinstance(node, FunctionCallNode):
            return self.evaluate_function_call(node)
        elif isinstance(node, ReturnNode):
            # Evaluate the return value and return it as a special return object
            return_value = self.evaluate(node.value)
            return ('RETURN', return_value)
        elif isinstance(node, UnaryOpNode):
            operand_val = self.evaluate(node.operand)
            if node.operator == '-':
                return -operand_val
            else:
                raise ValueError(f"Unknown unary operator: {node.operator}")
        else:
            raise ValueError(f"Unknown node type: {type(node)}")
        
    def evaluate_function_call(self, node):
        """Evaluate a function call"""
        if node.name not in self.functions:
            raise NameError(f"Function '{node.name}' is not defined")
        
        func_def = self.functions[node.name]
        
        # Check argument count
        if len(node.arguments) != len(func_def.parameters):
            raise ValueError(f"Function '{node.name}' expects {len(func_def.parameters)} arguments, got {len(node.arguments)}")
        
        # Evaluate arguments in the current (caller) scope
        arg_values = []
        for i, (param_type, param_name) in enumerate(func_def.parameters):
            arg_value = self.evaluate(node.arguments[i])
            # Type conversion based on parameter type
            if param_type == 'int':
                arg_value = int(arg_value)
            elif param_type == 'double':
                arg_value = float(arg_value)
            elif param_type == 'bool':
                arg_value = bool(arg_value)
            elif param_type == 'string':
                arg_value = str(arg_value)
            arg_values.append((param_type, param_name, arg_value))
        
        # Create a new scope for function execution, inheriting global variables
        old_variables = self.variables
        self.variables = old_variables.copy()  # Start with global variables
        
        # Bind arguments to parameters in the new scope (shadow globals if needed)
        for param_type, param_name, arg_value in arg_values:
            self.variables[param_name] = {'value': arg_value, 'type': param_type}
        
        # Execute function body
        result = None
        for statement in func_def.code_block:
            result = self.evaluate(statement)
            # Check for return statement
            if isinstance(result, tuple) and result[0] == 'RETURN':
                result = result[1]
                break
        
        # Restore original variables
        self.variables = old_variables
        
        return result


def test_interpreter():
    """Test the complete Salt pipeline: tokenize -> parse -> interpret"""
    test_cases = [
        "make int x 5",
        "make string name \"Salt\"",
        "make bool flag TRUE",
        "x + 10",
        "make int doubled x * 2"
    ]
    
    print("Testing complete Salt interpreter:")
    print("=" * 50)
    
    interpreter = Interpreter()
    
    for expression in test_cases:
        try:
            print(f"\nExpression: {expression}")
            
            # Step 1: Tokenize
            tokens = tokenize(expression)
            print(f"Tokens: {tokens}")
            
            # Step 2: Parse
            parser = Parser(tokens)
            ast = parser.parse()
            print(f"AST: {ast}")
            
            # Step 3: Interpret
            result = interpreter.evaluate(ast)
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 30)
    
    # Show all variables
    print(f"\nVariables in memory: {interpreter.variables}")


if __name__ == "__main__":
    test_interpreter() 
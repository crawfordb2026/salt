from interpreter import Interpreter
from math_parser import Parser, PrintNode, ArrayNode
from tokenizer import tokenize
import io
import sys

class WebInterpreter(Interpreter):
    def __init__(self):
        super().__init__()
        self.output_buffer = []
    
    def evaluate(self, node):
        """Override evaluate to capture print output"""
        if isinstance(node, PrintNode):
            # Capture print output
            values = []
            for expr in node.expressions:
                value = self.evaluate(expr)
                values.append(str(value))
            
            result = ''.join(values)
            self.output_buffer.append(result)
            return result
        else:
            return super().evaluate(node)

def run_salt_code(code):
    """Run Salt code and return output"""
    try:
        # Parse the code using the same strategy as the main interpreter
        tokens = tokenize(code)
        parser = Parser(tokens)
        
        # Create interpreter and run
        interpreter = WebInterpreter()
        
        # Parse and execute statements one by one, just like the main interpreter
        while parser.position < len(tokens):
            statement = parser.parse_statement()
            if statement is not None:
                try:
                    result = interpreter.evaluate(statement)
                    if result is not None and result not in [interpreter.SKIP, interpreter.END]:
                        # Don't print None results or control flow objects
                        pass
                except Exception as e:
                    return f"Error: {str(e)}", False
        
        # Combine all output
        output = '\n'.join(interpreter.output_buffer)
        if not output:
            output = "Code executed successfully (no output)"
        
        return output, True
        
    except Exception as e:
        return f"Error: {str(e)}", False

if __name__ == "__main__":
    # Test the web interpreter
    test_code = """
make int x 10
make int y 5
print "x = " x
print "y = " y
print "x + y = " x + y
"""
    
    output, success = run_salt_code(test_code)
    print("Success:", success)
    print("Output:")
    print(output) 
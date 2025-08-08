from web_interpreter import run_salt_code
from tokenizer import tokenize

# Test with the same code from test_for.salt
test_code = """# Array Operations
make int array scores[4]
make scores[0] 85
make scores[1] 92
make scores[2] 78
make scores[3] 96

print "Student Scores:"
make int i 0
loop i from 0 to 3
{
    print "Student " i + 1 ": " scores[i]
}

# Calculate average
make double total 0.0
make int j 0
loop j from 0 to 3
{
    make total total + scores[j]
}
make double average total / 4.0
print "Average score: " average"""

print("Testing web interpreter with test_for.salt code:")
print("=" * 50)

# Debug: Check tokens
tokens = tokenize(test_code)
print("Tokens:", tokens[:20])  # Show first 20 tokens

output, success = run_salt_code(test_code)
print(f"Success: {success}")
print(f"Output:\n{output}") 
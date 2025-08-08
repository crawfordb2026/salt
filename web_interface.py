from flask import Flask, render_template, request, jsonify
from web_interpreter import run_salt_code

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    try:
        code = request.json['code']
        
        # Run the Salt code using our web interpreter
        output, success = run_salt_code(code)
        
        return jsonify({'output': output, 'success': success})
        
    except Exception as e:
        return jsonify({'output': f'Server error: {str(e)}', 'success': False})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
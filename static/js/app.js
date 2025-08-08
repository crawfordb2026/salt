// Define a simple Salt mode for CodeMirror
CodeMirror.defineSimpleMode('salt', {
  start: [
    { regex: /#.*/, token: 'comment' },
    { regex: /"(?:[^"\\]|\\.)*"/, token: 'string' },
    { regex: /\b\d+(?:\.\d+)?\b/, token: 'number' },
    { regex: /\b(?:make|function|takes|gives|give|if|else|loop|while|from|to|by|skip|end|print|and|or|not)\b/, token: 'keyword' },
    { regex: /\b(?:int|double|string|bool)\b/, token: 'def' },
    { regex: /\b(?:TRUE|FALSE)\b/, token: 'atom' },
    { regex: /\b(?:eq|neq|gt|lt|gteq|lteq)\b/, token: 'keyword' },
    { regex: /\b[a-zA-Z_][a-zA-Z0-9_]*\b/, token: 'variable-3' },
    { regex: /[+\-*/%=]/, token: 'operator' },
    { regex: /[\[\]{}(),]/, token: 'bracket' }
  ] 
});

let editor;

document.addEventListener('DOMContentLoaded', function () {
  const ta = document.getElementById('codeEditor');
  editor = CodeMirror.fromTextArea(ta, {
    mode: 'salt',
    theme: 'monokai',
    lineNumbers: true,
    lineWrapping: true,
    indentUnit: 4,
    tabSize: 4,
    indentWithTabs: false,
    autofocus: false,
    value: ''
  });
  editor.setSize('100%', '100%');
  editor.getWrapperElement().setAttribute('spellcheck', 'false');
});

function scrollToBottom() {
  const terminal = document.querySelector('.terminal');
  if (terminal) terminal.scrollTop = terminal.scrollHeight;
}

function showSection(sectionName) {
  document.querySelectorAll('.section').forEach((s) => s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach((b) => b.classList.remove('active'));
  document.getElementById(sectionName).classList.add('active');
  event.target.classList.add('active');
  if (sectionName === 'ide' && editor) setTimeout(() => editor.refresh(), 0);
}

function runCode() {
  const code = editor ? editor.getValue() : document.getElementById('codeEditor').value;
  const output = document.getElementById('output');
  const runBtn = document.getElementById('runBtn');
  if (!code.trim()) {
    output.innerHTML += '\n❌ No code to run!';
    return;
  }
  runBtn.disabled = true;
  runBtn.textContent = '⏳ Running...';
  output.innerHTML += '\n\n🔄 Running code...\n';
  scrollToBottom();
  fetch('/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code })
  })
    .then((r) => r.json())
    .then((data) => {
      output.innerHTML += '\n' + (data.success ? '✅ ' : '❌ ') + data.output + '\n';
      setTimeout(scrollToBottom, 50);
    })
    .catch((err) => {
      output.innerHTML += '\n❌ Error: ' + err.message + '\n';
      setTimeout(scrollToBottom, 50);
    })
    .finally(() => {
      runBtn.disabled = false;
      runBtn.textContent = '▶ Run Code';
      setTimeout(scrollToBottom, 100);
    });
}

function clearOutput() {
  document.getElementById('output').innerHTML = '';
}

function loadExample() {
  const examples = [
    `# Simple Calculator
 make int a 10
 make int b 5
 print "a = " a
 print "b = " b
 print "a + b = " a + b
 print "a - b = " a - b
 print "a * b = " a * b
 print "a / b = " a / b`,

    `# Array Operations
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
 print "Average score: " average`,

    `# Function Example
 make function factorial takes int n gives int
 {
     if n lteq 1
     {
         give 1
     }
     else
     {
         give n * factorial(n - 1)
     }
 }
 
 make int result factorial(5)
 print "5! = " result`,

    `# Loop Control Example
 make int i 0
 loop i from 1 to 10
 {
     if i eq 5
     {
         skip
     }
     if i eq 8
     {
         end
     }
     print "Number: " i
 }
 print "Loop finished"`
  ];
  const randomExample = examples[Math.floor(Math.random() * examples.length)];
  if (editor) editor.setValue(randomExample);
  else document.getElementById('codeEditor').value = randomExample;
}

function loadCompleteExample() {
  const code = `# Simple Salt program demonstrating various features
 make int x 10
 make int y 5
 make string message "Comparison result"
 
 # Function definition
 make function max takes int a, int b gives int
 {
     if a gt b
     {
         give a
     }
     else
     {
         give b
     }
 }
 
 # Loop demonstration
 make int i 0
 loop i from 1 to 5
 {
     if i eq 3
     {
         skip
     }
     print "Loop iteration:" i
 }
 
 # Function call
 make int maximum max(x, y)
 print "Maximum value is:" maximum
 
 if x gt y
 {
     print message ": x is greater than y"
     print "Values: x = " x ", y = " y
 }
 else
 {
     print message ": y is greater than or equal to x"
 }
 
 print "Program finished"`;
  showSection('ide');
  if (editor) {
    editor.setValue(code);
    editor.refresh();
  } else {
    document.getElementById('codeEditor').value = code;
  }
}

// Ctrl/Cmd+Enter runs code
document.addEventListener('keydown', function (e) {
  const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
  const meta = isMac ? e.metaKey : e.ctrlKey;
  if (meta && e.key === 'Enter') {
    e.preventDefault();
    runCode();
  }
}); 
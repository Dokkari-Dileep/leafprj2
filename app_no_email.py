"""
App that saves feedback locally without email
"""

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "aJPsrKrxlGlGEXb0jFSNY"

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>AgriDetect - No Email Version</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .success { color: green; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>AgriDetect - Feedback System</h1>
        <p><strong>Note:</strong> Email system is disabled. Feedback is saved locally only.</p>
        
        <h3>Submit Feedback</h3>
        <form id="feedbackForm">
            <p>Name: <input type="text" name="name" required></p>
            <p>Email: <input type="email" name="email" required></p>
            <p>Message: <textarea name="message" rows="4" required></textarea></p>
            <button type="submit">Submit</button>
        </form>
        
        <div id="result"></div>
        
        <script>
            document.getElementById('feedbackForm').onsubmit = async (e) => {
                e.preventDefault();
                const form = e.target;
                const data = {
                    name: form.name.value,
                    email: form.email.value,
                    message: form.message.value,
                    category: 'feedback',
                    subject: 'Feedback from form'
                };
                
                const response = await fetch('/submit-feedback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                document.getElementById('result').innerHTML = 
                    result.success ? 
                    '<p class="success">✅ ' + result.message + '</p>' :
                    '<p class="error">❌ ' + result.message + '</p>';
            };
        </script>
    </body>
    </html>
    """

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        
        # Save to file
        if not os.path.exists('feedback_data'):
            os.makedirs('feedback_data')
        
        filename = f"feedback_data/feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': data
            }, f, indent=2)
        
        # Also save to main log
        log_file = 'feedback_data/all_feedback.json'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    all_data = json.load(f)
                except:
                    all_data = []
        else:
            all_data = []
        
        all_data.append({
            'timestamp': datetime.now().isoformat(),
            'data': data
        })
        
        with open(log_file, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Feedback saved successfully! File: {filename}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting app without email...")
    print("🌐 Open: http://localhost:5000")
    app.run(debug=True, port=5000)
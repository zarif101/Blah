from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import get_info
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        task = request.form.get('task')
        # Here, you can process the phone number and task as needed
        # For now, we'll just render the same page with a message
        message = f"Phone Number: {phone_number}, Task: {task}"
        args = ['--phone_number', phone_number,'--prompt',task,'--preload_whisper','--start_ngrok']
        session['phone_number'] = phone_number
        session['task'] = task
        session['messages'] = []
        result = subprocess.run(['python', 'make_calls.py'] + args, capture_output=True, text=True)
        print(result)
        #return render_template('index.html', message=message)
        return redirect(url_for('query'))
        
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        user_query = request.form['query']
        # Process the query and generate a response
        response=get_info.main(user_query)
        response = f"Response to your query: {response}"
        
        # Retrieve existing messages from the session
        messages = session.get('messages', [])
        # Add the new query and response to the message history
        messages.append({'type': 'user', 'text': user_query})
        messages.append({'type': 'response', 'text': response})
        
        # Save updated message history to the session
        session['messages'] = messages
        
        return render_template('query.html', messages=messages, phone_number=session.get('phone_number', ''), task=session.get('task', ''))

    # Retrieve message history from the session
    messages = session.get('messages', [])
    
    return render_template('query.html', messages=messages, phone_number=session.get('phone_number', ''), task=session.get('task', ''))

if __name__ == '__main__':
    app.run(debug=True)

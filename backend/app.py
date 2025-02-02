from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from openai import OpenAI

app = Flask(__name__)
app.secret_key = 'your_secret_key'

openai = OpenAI(api_key='placeholder')

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    role = request.form.get('role')
    session['userRole'] = role
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user_role = session.get('userRole', 'guest')
    return render_template('dashboard.html', user_role=user_role)

@app.route('/openai_chat')
def openai_chat():
    return render_template('openai_chat.html')

@app.route('/last_diagram_page')
def last_diagram_page():
    return render_template('last_diagram_page.html')

@app.route('/openai_process_chat', methods=['POST'])
def openai_process_chat():
    data = request.get_json()
    user_input = data['message']
    response = openai.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal:food-nutrition:98b6QDQw",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    assistant_message = response.choices[0].message.content
    return jsonify({'response': assistant_message})

@app.route('/import_export')
def import_export():
    return render_template('import_export.html')

@app.route('/get_content/<country_code>/<category>')
def get_content(country_code, category):
    template_name = f"{country_code}_{category}.html"
    return render_template(template_name)

if __name__ == '__main__':
    app.run(debug=True)

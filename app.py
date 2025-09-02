from flask import Flask, request, render_template
import os

app = Flask(__name__)

def process_input(user_input):
    # 🔒 Your hidden logic
    if (user_input.isdigit()):
        val = int(user_input)
        if (val % 4 == 0):
            return val * 2 + 16
        else:
            return val * 2
    return user_input[::-1]  # Example: reverse the input

@app.route('/', methods=['GET', 'POST'])
def home():
    output = ''
    if request.method == 'POST':
        user_input = request.form['user_input']
        output = process_input(user_input)
    return render_template('index.html', output=output)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

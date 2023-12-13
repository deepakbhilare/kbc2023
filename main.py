from flask import Flask, render_template, request
import random
import os
import sys
import csv
from io import StringIO



app = Flask(__name__)

# Use absolute paths to the CSV files
questions_file = os.path.abspath('/Users/abhay/Documents/flask/website/questions.csv')
options_file = os.path.abspath('/Users/abhay/Documents/flask/website/options.csv')

# Load questions from the CSV file
question_data = []

with open(questions_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 2:
            question = row[1]
            question_data.append({
                'question': question,
            })

@app.template_filter('next_char')
def next_char(s):
    print(chr(ord(s) + 1))
    return chr(ord(s) + 1)

# Load options from the CSV file
options_data = []

with open(options_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        options = [option.strip() for option in row]
        options_data.append(options)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    if request.method == 'POST':
        username = request.form['username']
        random_index = random.randint(0, len(question_data) - 1)
        question = question_data[random_index]['question']
        options = options_data[random_index]


        if 'answer' in request.form:
            print(str(random_index) + ' : ' + request.form['answer'])

        return render_template('quiz.html', username=username, question=question, options=options)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



# main.py

from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import sys

sys.path.append('/path/to/game_module_directory')
import game

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    username = request.form['username']
    if request.method == 'POST':
        username = request.form['username']
        
        user_answer = request.form.get('answer')
        current_question=game.getQuestion()
        current_options=game.getOption()
        print("user_answer:",user_answer)
        game.check_answer(request.form.get('answer') )




        return render_template('quiz.html', username=username, question=current_question, options=current_options, useranswer=user_answer)

    #return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
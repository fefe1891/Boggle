from flask import Flask, request, render_template, redirect, flash, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "your-secret-key"

boggle_game = Boggle()

@app.route('/')
def home():
    """ Show the home page with a new board """
    board = boggle_game.make_board()
    session['board'] = board
    topscore = session.get("topscore", 0)
    times_played = session.get("times_played", 0)
    session['times_played'] = times_played
    print(session)
    
    return render_template('base.html', board=board, topscore=topscore, times_played=times_played)



@app.route('/check-word')
def check_word():
    """Check if word is in the dictionary"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    
    return jsonify({"result": response})



@app.route('/submit-score', methods=["POST"])
def submit_score():
    score = request.json["score"]
    topscore = session.get("topscore", 0)
    times_played = session.get("times_played", 0)
    
    session["topscore"] = max(score, topscore)
    session["times_played"] = times_played + 1
    
    return jsonify(beatHighScore=score > topscore)
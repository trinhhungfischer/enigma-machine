import traceback
from flask import Flask, render_template, request, jsonify, Response
from enigma.enigma import Enigma

app = Flask(__name__, template_folder='templates')
enigma = Enigma()

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False) 
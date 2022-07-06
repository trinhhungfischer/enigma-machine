import traceback
from flask import Flask, render_template, request, jsonify, Response
from enigma.enigma import Enigma

app = Flask(__name__, template_folder='templates')
enigma = Enigma()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/rotor_order', methods=['GET', 'POST'])
def rotor_order():
  rotor1 = request.form['1']
  rotor2 = request.form['2']
  rotor3 = request.form['3']
  if ((rotor1 =='') | (rotor2 == '') | (rotor3 == '')):
    rotor1 = 1
    rotor2 = 2
    rotor3 = 3
  
  rotor1 = int(rotor1)
  rotor2 = int(rotor2)
  rotor3 = int(rotor3)
  
  enigma.set_rotor_order((rotor1, rotor2, rotor3))
  
  results = {1: rotor1, 2: rotor2, 3: rotor3}
  return jsonify(result = results)
    
@app.route('/rotor_setting', methods=['GET', 'POST'])
def rotor_setting():
  rotor1 = request.form['1']
  rotor2 = request.form['2']
  rotor3 = request.form['3']
  
  if ((rotor1 =='') | (rotor2 == '') | (rotor3 == '')):
    rotor1 = 1
    rotor2 = 1
    rotor3 = 1
  
  rotor1 = int(rotor1)
  rotor2 = int(rotor2)
  rotor3 = int(rotor3)
  
  enigma.set_rotor_setting((rotor1 - 1, rotor2 - 1, rotor3 - 1))


  results = {1: rotor1, 2: rotor2, 3: rotor3}
  return jsonify(result = results)

@app.route('/plugboard', methods=['GET', 'POST'])

def plugboard():
  plugboard = request.form['value']
  print(plugboard)
  enigma.set_plugboard(plug_boards=plugboard)

  results = {"value" : plugboard}
  return jsonify(result = results)
  

@app.route('/reflector', methods=['GET', 'POST'])

def reflector():
  reflector = request.form['value']
  print(reflector)
  enigma.set_reflector(reflectors=reflector)

  results = {"value" : reflector}
  return jsonify(result = results)

@app.route('/letter', methods=['GET', 'POST'])

def letter():
  letter = request.form['value']
  print(letter)
  letter = enigma.encode(letter)
  results = {"value" : letter}
  return jsonify(result = results)

if __name__ == '__main__':
    app.run(debug=False)


import os, data.recomendation_loader
from flask import Flask, redirect, render_template, request, url_for

os.system('cls')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data={'titulo': 'Index', 'bienvenida': 'Saludos.', 'aviso': 'Para darle recomendación alguna, por favor, ingrese su ID de cliente.'})

@app.route('/recomendado/<client_id>')
def recomendado(client_id):
    client_id = int(client_id)
    recommendations = data.recomendation_loader.recommend_products(client_id, 5)
    return render_template('recomendado.html', data={'titulo': 'Recomendado', 'client_id': client_id, 'recommendations': recommendations})

@app.route('/enviar', methods=['POST'])
def enviar():
    client_id = request.form['client_id_input']
    return redirect(url_for('recomendado', client_id=client_id))

def not_found(error):
    return render_template('404.html'), 404
    # return redirect(url_for('index'))

if __name__ == '__main__':
    app.register_error_handler(404, not_found)
    app.run(debug=True, port=5000)

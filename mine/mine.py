from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from io import BytesIO
from cryptography.fernet import Fernet
import os

# Génération et stockage sécurisé de la clé de chiffrement
key = Fernet.generate_key()
cipher_suite = Fernet(key)

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète_ici'

eraz_log_file_path = "eraz_log.txt"
base_number = 751953751953

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        eraz_id = request.form.get('eraz_id')
        if eraz_id.isdigit() and is_id_valid_and_unique(int(eraz_id)):
            return generate_and_send_eraz(int(eraz_id))
        else:
            flash('ID invalide ou déjà utilisé.', 'danger')
        return redirect(url_for('index'))
    
    mined_ids = get_mined_ids()
    return render_template('index.html', mined_ids=mined_ids)

def is_id_valid_and_unique(eraz_id):
    if eraz_id % base_number != 0:
        return False
    with open(eraz_log_file_path, 'r') as file:
        used_ids = file.read().splitlines()
    return str(eraz_id) not in used_ids

def generate_and_send_eraz(eraz_id):
    content = f"ID de l'eraz: {eraz_id}"
    encrypted_content = cipher_suite.encrypt(content.encode())
    eraz_file = BytesIO(encrypted_content)
    add_eraz_id_to_log(eraz_id)
    return send_file(eraz_file, as_attachment=True, attachment_filename=f"{eraz_id}.eraz", mimetype='text/plain')

def add_eraz_id_to_log(eraz_id):
    with open(eraz_log_file_path, 'a') as file:
        file.write(f"{eraz_id}\n")

def get_mined_ids():
    if os.path.exists(eraz_log_file_path):
        with open(eraz_log_file_path, 'r') as file:
            return file.read().splitlines()
    return []

if __name__ == '__main__':
    if not os.path.exists(eraz_log_file_path):
        open(eraz_log_file_path, 'w').close()
    app.run(debug=True)

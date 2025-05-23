from flask import Flask, request, jsonify,render_template,send_from_directory
import os
from ecriture_et_lecture import*

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route('/')
def index():
    return render_template('interface.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    caesar_key = request.form.get('caesarKey', '')
    
    if ('audioFile' not in request.files) :
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400

    audio_file = request.files['audioFile']
    hidden_message = request.form.get('hiddenMessage', '')
    caesar_key = request.form.get('caesarKey', '')
    readOrWrite =request.form.get('readOrWrite','')
    
    if audio_file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    if audio_file:
        # Sauvegarder le fichier dans le dossier upload
        audio_file.save(os.path.join(UPLOAD_FOLDER, audio_file.filename))

        if int(readOrWrite)==0 :

            if caesar_key!="" :

                path_modif=steganographie(os.path.join(UPLOAD_FOLDER, audio_file.filename),str(hidden_message),int(caesar_key))
            else :

                path_modif=steganographie(os.path.join(UPLOAD_FOLDER, audio_file.filename),str(hidden_message))

            return jsonify({'new_file_name': os.path.basename(path_modif)}), 200
        elif int(readOrWrite)==1 :

            if caesar_key!="" :

                message = lecture(os.path.join(UPLOAD_FOLDER, audio_file.filename), int(caesar_key))
            else :

                message = lecture(os.path.join(UPLOAD_FOLDER, audio_file.filename))
            return jsonify({"message": message})




@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
 
    
    

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify; import openpyxl
from openpyxl import Workbook ;import os
from datetime import datetime

app = Flask(__name__)

# Configurer le dossier pour les photos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EXCEL_FILE = 'interventions.xlsx'

if not os.path.exists(EXCEL_FILE):
    wb = Workbook()
    ws = wb.active
    ws.title = "Interventions"
    ws.append([
        "Date de saisie",
        "Technicien",
        "Lieu d’intervention",
        "Équipement concerné",
        "Entreprise intervenante",
        "Motif d’intervention",
        "Opération réalisée",
        "Opération terminée",
        "Photo"
    ])
    wb.save(EXCEL_FILE)

@app.route('/save', methods=['POST'])
def save_data():
    try:
        # Récupérer les données du formulaire
        date = request.form['date']
        technicien = request.form['technicien']
        lieu = request.form['lieu']
        equipement = request.form['equipement']
        entreprise = request.form['entreprise']
        motif = request.form['motif']
        operation = request.form['operation']
        terminee = request.form['terminee']
        
        # Gestion de la photo
        photo_file = request.files.get('photo')
        photo_path = ''
        if photo_file:
            # Sauvegarder la photo dans le dossier des uploads
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            photo_filename = f"{timestamp}_{photo_file.filename}"
            photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
            photo_file.save(photo_path)

        # Sauvegarder les données dans le fichier Excel
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active
        ws.append([
            date,
            technicien,
            lieu,
            equipement,
            entreprise,
            motif,
            operation,
            terminee,
            photo_path
        ])
        wb.save(EXCEL_FILE)

        return jsonify({"message": "Données enregistrées avec succès."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

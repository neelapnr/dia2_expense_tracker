# dia2_expense_tracker

Application de gestion de notes de frais avec IA.

Le projet permet d’analyser une image de ticket de caisse ou de facture, d’extraire automatiquement les informations importantes grâce à un modèle IA, puis d’enregistrer les données dans Google Sheets.

---

## Technologies utilisées

- Python
- FastAPI
- HTMX
- Groq API (Llama 4 Scout)
- Google Sheets API
- HTML / CSS / JavaScript

---

## Fonctionnalités

- Upload d’image
- Preview de l’image
- Extraction automatique des données avec IA
- Formulaire modifiable manuellement
- Envoi des données vers Google Sheets
- Interface web simple en dark mode

---

## Structure du projet

expense-tracker/
│
├── app.py
├── backend.py
├── sheets.py
├── context.txt
├── prompt.txt
├── requirements.txt
├── .env
│
└── static/
    ├── index.html
    ├── style.css
    └── app.js

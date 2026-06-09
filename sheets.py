import os
from datetime import datetime

import gspread

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials


class GoogleSheetsClient:

    def __init__(self):

        load_dotenv()

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"),
            scopes=scopes
        )

        self.client = gspread.authorize(creds)

        self.sheet = self.client.open_by_key(
            os.getenv("GOOGLE_SHEET_ID")
        )

        self.worksheet = self.sheet.worksheet("Notes de frais")

    def append_expense(self, data, image_url=None):

        row = [
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            data.get("type_document"),
            data.get("fournisseur"),
            data.get("date"),
            data.get("montant_ttc"),
            data.get("tva"),
            data.get("devise"),
            data.get("description"),
            data.get("confiance"),
            image_url
        ]

        self.worksheet.append_row(row)

if __name__ == "__main__":

    client = GoogleSheetsClient()

    client.append_expense({
        "type_document": "restaurant",
        "fournisseur": "McDonalds",
        "date": "08/06/2026",
        "montant_ttc": 12.5,
        "tva": 2.1,
        "devise": "EUR",
        "description": "Repas midi",
        "confiance": "haute"
    })

    print("OK")

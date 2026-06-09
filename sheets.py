import os

from datetime import datetime

import gspread

from dotenv import load_dotenv

from google.oauth2.service_account import Credentials


load_dotenv()


class GoogleSheetsClient:

    def __init__(self):

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets"
        ]

        creds = Credentials.from_service_account_file(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"),
            scopes=scopes
        )

        client = gspread.authorize(creds)

        sheet = client.open_by_key(
            os.getenv("GOOGLE_SHEET_ID")
        )

        self.worksheet = sheet.worksheet("Notes de frais")

    def append_expense(self, data):

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

            ""
        ]

        self.worksheet.append_row(row)

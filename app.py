from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend import ExpenseAgent
from sheets import GoogleSheetsClient


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


agent = ExpenseAgent()

sheets_client = GoogleSheetsClient()


@app.get("/", response_class=HTMLResponse)
async def home():

    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):

        return """
        <div class="error">
            Fichier invalide
        </div>
        """

    image_bytes = await file.read()

    result = agent.extract_from_bytes(
        image_bytes,
        file.content_type
    )

    return f"""

    <form
        hx-post="/api/submit"
        hx-target="#confirmation"
        hx-swap="innerHTML"
    >

        <label>Type</label>

        <input
            type="text"
            name="type_document"
            value="{result.get("type_document", "")}"
        >

        <label>Fournisseur</label>

        <input
            type="text"
            name="fournisseur"
            value="{result.get("fournisseur", "")}"
        >

        <label>Date</label>

        <input
            type="text"
            name="date"
            value="{result.get("date", "")}"
        >

        <label>Montant TTC</label>

        <input
            type="text"
            name="montant_ttc"
            value="{result.get("montant_ttc", "")}"
        >

        <label>TVA</label>

        <input
            type="text"
            name="tva"
            value="{result.get("tva", "")}"
        >

        <label>Devise</label>

        <input
            type="text"
            name="devise"
            value="{result.get("devise", "")}"
        >

        <label>Description</label>

        <input
            type="text"
            name="description"
            value="{result.get("description", "")}"
        >

        <label>Confiance</label>

        <input
            type="text"
            name="confiance"
            value="{result.get("confiance", "")}"
        >

        <button type="submit">
            Envoyer
        </button>

    </form>
    """


@app.post("/api/submit", response_class=HTMLResponse)
async def submit(

    type_document: str = Form(None),
    fournisseur: str = Form(None),
    date: str = Form(None),
    montant_ttc: str = Form(None),
    tva: str = Form(None),
    devise: str = Form(None),
    description: str = Form(None),
    confiance: str = Form(None)

):

    data = {

        "type_document": type_document,
        "fournisseur": fournisseur,
        "date": date,
        "montant_ttc": montant_ttc,
        "tva": tva,
        "devise": devise,
        "description": description,
        "confiance": confiance
    }

    sheets_client.append_expense(data)

    return """
    <div class="success">
        Note ajoutée dans Google Sheets
    </div>
    """

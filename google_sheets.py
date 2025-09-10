import gspread
from google.oauth2.service_account import Credentials

# Définir la portée nécessaire pour gspread
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Authentification
def get_worksheet():
    creds = Credentials.from_service_account_file(
        "credentials/google_service_account.json",
        scopes=SCOPES
    )
    gc = gspread.authorize(creds)
    sh = gc.open("TaxiBookings")  # Nom exact de la Google Sheet
    ws = sh.sheet1
    return ws

def append_booking(data):
    """
    Ajoute une réservation unique dans Google Sheet.
    Evite les lignes vides ou doublons directs.
    """
    ws = get_worksheet()

    # Vérifier si la ligne existe déjà (simple comparaison)
    all_rows = ws.get_all_values()
    if data in all_rows:
        return  # Ne rien faire si identique

    ws.append_row(data, value_input_option="USER_ENTERED")

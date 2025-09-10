import gspread

def get_worksheet():
    gc = gspread.service_account(filename="credentials/google_service_account.json")
    sh = gc.open("TaxiBookings")  # Remplacez par le nom de votre Google Sheet
    ws = sh.sheet1
    return ws

def append_booking(data):
    ws = get_worksheet()
    ws.append_row(data)

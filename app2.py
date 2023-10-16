import gspread

gc = gspread.service_account(filename="credentials.json")

sheet = gc.open("Remote_bot")
print("done")
# worksheet = sheet.worksheet("Sheet1")

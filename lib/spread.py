import gspread
from oauth2client.service_account import ServiceAccountCredentials as sacred
import pandas as pd
import os

SA_KEY_FILE = os.getenv("SA_KEY_FILE", default="sa-key.json")
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
DEFAULT_ROW = 100
DEFAULT_COL = 26
gc = gspread.authorize(sacred.from_json_keyfile_name(SA_KEY_FILE, SCOPE))


def _get_sheet(worksheet, title):
    worksheets = gc.open(worksheet)
    if title not in (x.title for x in worksheets.worksheets()):
        worksheets.add_worksheet(title=title, rows=DEFAULT_ROW, cols=DEFAULT_COL)
    return worksheets.worksheet(title)


def read_df(worksheet, title):
    worksheet = _get_sheet(worksheet, title)
    return pd.DataFrame(worksheet.get_all_records())


def update_df(worksheet, df, title):
    worksheet = _get_sheet(worksheet, title)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

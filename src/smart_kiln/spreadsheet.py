import os.path
import gspread
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


TOKEN = "token.json"


class SpredsheetManager:
    """
    Sets up a connection to a google spreadsheet

    To get the token.json file please follow the instructions here:
    https://docs.gspread.org/en/latest/oauth2.html


    Args:
        spread_sheet_name (str): The name of the spreadsheet to connect to
        token_file (str): The path to the token.json file. Defaults to TOKEN
    """

    def __init__(self, spread_sheet_name, token_file=TOKEN, base_offset=2):
        self.spread_sheet_name = spread_sheet_name
        self.token_file = token_file
        self.gc = gspread.service_account(self.token_file)
        self.spreadsheet = self.gc.open(self.spread_sheet_name)
        self.base_offset = base_offset

        self.current_worksheet = None
        self.current_offset = base_offset

    def open_recording_session(self, name):
        """
        Creates a new worksheet with the given name and sets it as the current
        The offset will be set to 1
        """

        self.current_worksheet = self.spreadsheet.add_worksheet(title=name, rows="100", cols="20")
        self.current_offset = self.base_offset

    def open_recording_session_from_base_sheet(self, name, base_sheet="BaseSheet"):
        """
        Creates a new worksheet with the given name and sets it as the current
        The offset will be set to 1
        """

        # self.current_worksheet = self.spreadsheet.duplicate_sheet(source_sheet_id=base_sheet, insert_sheet_index=0, new_sheet_id=None, new_sheet_name=name)
        base_sheet = self.spreadsheet.worksheet(base_sheet)
        self.current_worksheet = base_sheet.duplicate(new_sheet_name=name)
        self.current_offset = 2

    def append(self, data):
        """
        Appends the datetime to cell A_n and the data to cell B_n
        """
        self.current_worksheet.update(f"A{self.current_offset}", str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.current_worksheet.update(f"B{self.current_offset}", data)
        self.current_offset += 1

        logger.debug(f"Appended {data} to {self.current_worksheet.title}")
        logger.debug(f"Current offset is {self.current_offset}")

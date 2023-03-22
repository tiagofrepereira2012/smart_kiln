from smart_kiln.spreadsheet import SpredsheetManager
import unittest

class TestSpreadSheetManage(unittest.TestCase):
    
    def test_append(self):
        spreadsheet = SpredsheetManager("kiln_measurements")
        spreadsheet.open_recording_session_from_base_sheet("test")
        spreadsheet.append(22)
        spreadsheet.append(40)
        spreadsheet.append(43)
        spreadsheet.append(54)
        spreadsheet.append(55)
        
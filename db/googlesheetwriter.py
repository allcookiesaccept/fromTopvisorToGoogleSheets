import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import List, Dict


class GoogleSheetsManager:
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        """
        Initialize the Google Sheets Manager.
        :param credentials_path: Path to the service account credentials JSON file.
        :param spreadsheet_id: ID of the Google Sheets document.
        """
        self.spreadsheet_id = spreadsheet_id
        self.service = self._initialize_service(credentials_path)

    def _initialize_service(self, credentials_path: str):
        """
        Initialize the Google Sheets API service.
        :param credentials_path: Path to the service account credentials JSON file.
        :return: Google Sheets API service object.
        """
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=scopes
        )
        return build("sheets", "v4", credentials=credentials)

    def read(self, sheet_name: str, range_name: str) -> List[List[str]]:
        """
        Read data from a specific range in the Google Sheet.
        :param sheet_name: Name of the sheet.
        :param range_name: Range of cells to read (e.g., "A1:E10").
        :return: List of rows, where each row is a list of cell values.
        """
        full_range = f"{sheet_name}!{range_name}"
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheet_id, range=full_range)
            .execute()
        )
        return result.get("values", [])

    def write(self, sheet_name: str, range_name: str, data: List[List[str]]):
        """
        Write data to a specific range in the Google Sheet.
        :param sheet_name: Name of the sheet.
        :param range_name: Range of cells to write (e.g., "A1:E10").
        :param data: List of rows, where each row is a list of cell values.
        """
        full_range = f"{sheet_name}!{range_name}"
        body = {"values": data}
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=full_range,
            valueInputOption="RAW",
            body=body,
        ).execute()

    def append(self, sheet_name: str, range_name: str, data: List[List[str]]):
        """
        Append data to the end of a specific range in the Google Sheet.
        :param sheet_name: Name of the sheet.
        :param range_name: Range of cells to append to (e.g., "A1:E1").
        :param data: List of rows, where each row is a list of cell values.
        """
        full_range = f"{sheet_name}!{range_name}"
        body = {"values": data}
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=full_range,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()

    def clear(self, sheet_name: str, range_name: str):
        """
        Clear data in a specific range in the Google Sheet.
        :param sheet_name: Name of the sheet.
        :param range_name: Range of cells to clear (e.g., "A1:E10").
        """
        full_range = f"{sheet_name}!{range_name}"
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id, range=full_range
        ).execute()
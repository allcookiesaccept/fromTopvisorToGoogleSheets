import pygsheets
import json
import pandas as pd

class GoogleSheetWriter:

    def __init__(self, service_file_path, spreadsheet_id, sheet_name):
        """
        :param service_file_path: str
        :param spreadsheet_id: str
        :param sheet_name: str
        """

        self.service_file_path = service_file_path
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name

    def oauth(self):

        self.oauth = pygsheets.authorize(service_file=self.service_file_path)

        return self.oauth

    def open_spreadsheet(self):

        self.spreadsheet = self.oauth.open_by_key(self.spreadsheet_id)
        print(f'Opening workbook')
        return self.spreadsheet


    def _add_worksheet(self):

        try:
            self.spreadsheet.add_worksheet(self.sheet_name)
        except:
            pass

    def _open_worksheet(self):

        self.worksheet = self.spreadsheet.worksheet_by_title(self.sheet_name)
        print(f'Opening {self.sheet_name} sheet in workbook')
        return self.worksheet

    def _clear_worksheet(self):
        print(f'Cleaning {self.sheet_name} in workbook')

        self.worksheet.clear('A1', None, '*')

    def _write_dataframe_to_google_worksheet(self, df):
        """
        :param df: DataFrame
        """
        print(f'Writing {self.sheet_name} in workbook')

        self.worksheet.set_dataframe(df, (1, 1), encoding='utf-8', fit=True)
        self.worksheet.frozen_rows = 1

    def run(self, df):

        self.oauth()
        self.open_spreadsheet()
        self._add_worksheet()
        self._open_worksheet()
        self._clear_worksheet()
        self._write_dataframe_to_google_worksheet(df)

def main():

    secret_key = 'pysheets-347309-9629095400b4.json'
    sheet_id = '1UmHsFGC6LiQEeuVCtGZPCB8VzkpVUaAvwQ9D9y5FS-w'
    sheet_name = 'channels'


if __name__ == '__main__':
    main()
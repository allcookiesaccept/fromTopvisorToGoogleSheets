import pandas as pd
import calendar
import locale
from datetime import datetime
import win32com.client
import os
from gsheets import GoogleSheetWriter
# https://stackoverflow.com/questions/40893870/refresh-excel-external-data-with-python



class ExcelDataframeMaker:

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        print('hello')
        self.on_off = ['online', 'offline']
        self.price_metrics = ['revenue', 'profit', 'checks_sum',
                              'checks', 'orders']
        self.sheet_names = {'channel_type': 'off_on', 'channels': 'by_channels'}
        self.service_file_path = 'pysheets-347309-9629095400b4.json'
        self.work_book_id = '1UmHsFGC6LiQEeuVCtGZPCB8VzkpVUaAvwQ9D9y5FS-w'
        self.channels = ['(none)', '(not set)', 'cpa', 'cpc', 'cpm', 'email', 'NA', 'organic', 'referral', 'trigger']
        self.channels_price_metrics = ['revenue', 'profit', 'aov', 'orders']
        self.excel_books = [
            '\\olap_channels.xlsx',
            '\\olap_online_offline.xlsx']

    def run(self):

        self._refresh_data()
        self._channel_type_dataframe_creator()
        self._channels_dataframe_creator()

    def _refresh_data(self):

        xlapp = win32com.client.DispatchEx("Excel.Application")
        print("Close Xlapp")

        for book in self.excel_books:
            print(f'Update {book}')
            wb = xlapp.workbooks.open(f'{self.base_path}{book}')
            wb.RefreshAll()
            wb.Save()

        print("Close Xlapp")
        xlapp.Quit()

    def _channel_type_dataframe_creator(self):

        reader = pd.read_excel('olap_online_offline.xlsx')
        header = reader.columns
        olap = pd.DataFrame(data=reader.iloc[11:30, 0:12], columns=header).reset_index(drop=True)
        olap = olap.fillna(0)

        for x, item in enumerate(olap['month']):
            olap['month'][x] = datetime.strptime(item, '%B').month

        cols = ['year', 'month']
        olap['date'] = olap[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")

        for price in self.price_metrics:
            for tip in self.on_off:
                for x, item in enumerate(olap[f'{tip}_{price}']):
                    olap[f'{tip}_{price}'][x] = str(item).replace(".", ',')

        sender = GoogleSheetWriter(self.service_file_path, self.work_book_id, self.sheet_names['channel_type'])

        sender.run(olap)

    def _channels_dataframe_creator(self):

        reader = pd.read_excel('olap_channels.xlsx')
        header = reader.columns
        olap = pd.DataFrame(data=reader.iloc[9:30,0:41], columns=header).reset_index(drop=True)
        olap = olap.fillna(0)

        for x, item in enumerate(olap['month']):
            olap['month'][x] = datetime.strptime(item, '%B').month

        cols = ['year', 'month']
        olap['date'] = olap[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")

        for channel in self.channels:
            for sum_type in self.channels_price_metrics:
                for x, item in enumerate(olap[f'{channel}_{sum_type}']):
                    olap[f'{channel}_{sum_type}'][x] = str(item).replace(".", ',')

        sender = GoogleSheetWriter(self.service_file_path, self.work_book_id, self.sheet_names['channels'])

        sender.run(olap)


def main():

    olap = ExcelDataframeMaker()

    olap.run()

if __name__ == '__main__':

    main()

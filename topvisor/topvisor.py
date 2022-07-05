import pygsheets
import json
import requests
import os
import datetime
from gsheets import GoogleSheetWriter
import pandas as pd

class Topvisor:

    def __init__(self):

        print('Authorizing Topvisor')
        self._initializing_dicts()
        self._get_credentials()
        self._set_dates()
        self._make_directories_for_json()
        self.headers = {'Content-type': 'application/json', 'User-Id': self.user, 'Authorization': f'bearer {self.key}'}
        self.server = 'https://api.topvisor.com'

        self.work_book_id = '10bQ3R1LvWd3QQW55ALaNOtdxLrZWdrz57Uhrhnu1bRw'
        self.service_file_path = 'D:\\pyprojects\\datastudio\\topvisor\\pysheets-347309-9629095400b4.json'

        self.summary_chart_api_url = '/v2/json/get/positions_2/summary_chart'
        self.keywords_api_url = '/v2/json/get/keywords_2/folders'

    def _initializing_dicts(self):

        self.se_region_index = {"yandex": 3, "google": 6}
        self.tags = {"commercial": 2}
        self.folders_dict = {
                  "iphone": 861539,
                  "ipad": 861590,
                  "mac": 861565,
                  "watch": 861584
                }
        self.metrics = ["avg", "visibility"]
        self.tops = ['all', '1_3', '1_10', '11_30']
        return self.se_region_index, self.tags, self.folders_dict, self.metrics

    def _set_dates(self):

        self.date_today = str(datetime.date.today())
        self.dates = ['2022-01-01', self.date_today]

        return self.dates, self.date_today

    def _get_credentials(self):

        self.user = ''
        self.key = ''
        self.project_id = ''

        with open('D:\\pyprojects\\datastudio\\topvisor\\login_data.txt', 'r', encoding='utf-8') as file:

            oauth_data = {}
            lines = file.read().splitlines()
            for line in lines:
                oauth_data[line.split(': ')[0]] = line.split(': ')[1]

            self.user = oauth_data['user']
            self.key = oauth_data['key']
            self.project_id = oauth_data['project_id']

            file.close()

        return self.user, self.key, self.project_id

    def _payload_generator(self, type, search_engine, tag=0, folder=''):

        if type == 'base':
            self.payload = {
                "project_id": self.project_id,
                "region_index": self.se_region_index[search_engine],
                "date1": self.dates[0],
                "date2": self.dates[-1],
                "type_range": 0,
                "show_visibility": True,
                "show_avg": True,
                "show_tops": True
            }
        elif type == 'folder':
            self.payload = {
                "project_id": self.project_id,
                "region_index": self.se_region_index[search_engine],
                "date1": self.dates[0],
                "date2": self.dates[-1],
                "type_range": 0,
                "show_visibility": True,
                "show_avg": True,
                "show_tops": True,
                "filters": [
                    {
                        "name": "group_folder_id",
                        "operator": "EQUALS",
                        "values": [
                            str(self.folders_dict[folder])
                        ]
                    }
                ],
                "group_folder_id_depth": "1"
            }
        elif type == 'tag':
            self.payload = {
                "project_id": self.project_id,
                "region_index": self.se_region_index[search_engine],
                "date1": self.dates[0],
                "date2": self.dates[-1],
                "type_range": 0,
                "show_visibility": True,
                "show_avg": True,
                "show_tops": True,
                "filters": [
                    {
                        "name": "tags",
                        "operator": "IN",
                        "values": [
                            str(tag)
                        ]
                    }
                ],
                "group_folder_id_depth": "1"
            }

        return self.payload

    def _make_directories_for_json(self):

        if not os.path.exists('D:\\pyprojects\\datastudio\\topvisor\\charts\\'):
            os.mkdir('D:\\pyprojects\\datastudio\\topvisor\\charts\\')

        if not os.path.exists('D:\\pyprojects\\datastudio\\topvisor\\charts\\summary\\'):
            os.mkdir('D:\\pyprojects\\datastudio\\topvisor\\charts\\summary\\')

        if not os.path.exists('D:\\pyprojects\\datastudio\\topvisor\\charts\\folders\\'):
            os.mkdir('D:\\pyprojects\\datastudio\\topvisor\\charts\\folders\\')

        if not os.path.exists('D:\\pyprojects\\datastudio\\topvisor\\charts\\tags\\'):
            os.mkdir('D:\\pyprojects\\datastudio\\topvisor\\charts\\tags\\')

    def get_groups_id(self):

        print(f'Requesting group folders id chart for')

        payload = {
            "project_id": self.project_id
        }
        self.response = requests.post(f'{self.server}{self.keywords_api_url}', headers=self.headers, data=json.dumps(payload))

        with open(f'topvisor/group_id.json', 'w', encoding='utf-8') as file:
            json.dump(self.response.json(), file, indent=4, ensure_ascii=False)
            file.close()

    def _get_folders_summary_charts(self):

        self.folders_summary_charts = {}

        for se in self.se_region_index.keys():
            for folder in self.folders_dict.keys():
                self._payload_generator(type='folder', search_engine=se,  folder=folder)
                get = self._get_response(type='folder', search_engine=se, folder=folder)
                self.folders_summary_charts[f'{se}_{folder}'] = get.json()
                self._save_response_to_json(type='folder', search_engine=se, folder=folder)

        return self.folders_summary_charts

    def _initialize_folder_frame(self):
        self.folder_frame = {
            'dates': [], 'yandex_iphone_avg': [], 'yandex_iphone_visibility': [],
            'yandex_ipad_avg': [], 'yandex_ipad_visibility': [], 'yandex_watch_avg': [],
            'yandex_watch_visibility': [],  'yandex_mac_avg': [], 'yandex_mac_visibility': [],
            'google_iphone_avg': [], 'google_iphone_visibility': [],
            'google_ipad_avg': [], 'google_ipad_visibility': [], 'google_watch_avg': [],
            'google_watch_visibility': [], 'google_mac_avg': [], 'google_mac_visibility': []
        }

        return self.folder_frame

    def _reformat_response_for_folders_summary_dataframe(self):
        self._initialize_folder_frame()


        for se in self.se_region_index.keys():
            for folder in self.folders_dict.keys():
                for metric in self.metrics:

                    self.folder_frame[f'{se}_{folder}_{metric}'] = \
                        self.folders_summary_charts[f'{se}_{folder}']["result"]["seriesByProjectsId"][self.project_id][metric]
                    for x, item in enumerate(self.folder_frame[f'{se}_{folder}_{metric}']):
                        self.folder_frame[f'{se}_{folder}_{metric}'][x] = str(item).replace(".", ",")
                    self.folder_frame["dates"] = \
                        self.folders_summary_charts[f'{se}_{folder}']["result"]["dates"]

        return self.folder_frame


    def get_summary_chart(self):

        for se in self.se_region_index.keys():
            self._payload_generator(search_engine=se, type='base')
            self._get_response(search_engine=se, type='base')
            self._save_response_to_json(se, 'base')

        # df = self._reformat_response_for_summary_dataframe()
        #
        # sheet_name = 'summary_test'
        # sender = GoogleSheetWriter(self.service_file_path, self.work_book_id, sheet_name)
        #
        # sender.run(df)

    def _get_response(self, search_engine, type, tag=0, folder=''):
        """

        :type search_engine: object
        """
        print(f'Requesting {type} summary chart for {search_engine}: {folder} : {tag}')
        self.response = requests.post(f'{self.server}{self.summary_chart_api_url}', headers=self.headers, data=json.dumps(self.payload))

        return self.response

    def _save_response_to_json(self, type, search_engine, tag=0, folder=''):

        if type == 'base':
            print(f'Saving /topvisor/charts/{self.date_today}-{search_engine}-summary-chart.json')
            with open(f'D:\\pyprojects\\datastudio\\topvisor\\charts\\{self.date_today}-{search_engine}-summary-chart.json', 'w', encoding='utf-8') as file:
                json.dump(self.response.json(), file, indent=4, ensure_ascii=False)
                file.close()
        elif type == 'folder':
            print(f'Saving /topvisor/charts/{self.date_today}-{search_engine}-{folder}-summary-chart.json')
            with open(f'topvisor/charts/{self.date_today}-{search_engine}-{folder}-summary-chart.json', 'w', encoding='utf-8') as file:
                json.dump(self.response.json(), file, indent=4, ensure_ascii=False)
                file.close()
        elif type == 'tag':
            print(f'Saving /topvisor/charts/{self.date_today}-{search_engine}-{tag}-summary-chart.json')
            with open(f'topvisor/charts/{self.date_today}-{search_engine}-summary-chart.json', 'w', encoding='utf-8') as file:
                json.dump(self.response.json(), file, indent=4, ensure_ascii=False)
                file.close()

    def _reformat_response_for_summary_dataframe(self):

        yandex = pd.read_json(f'topvisor/charts/{self.date_today}-yandex-summary-chart.json')
        google = pd.read_json(f'topvisor/charts/{self.date_today}-google-summary-chart.json')

        self.summary_frame = {
            "id": [], 'date': [], 'yandex_avg': [], 'google_avg': [], 'yandex_visibility': [],
            'google_visibility': [], 'yandex_all': [], 'yandex_1_3': [], 'yandex_1_10': [],
            'yandex_11_30': [], 'google_all': [], 'google_1_3': [], 'google_1_10': [],
            'google_11_30': []
        }

        for x in range(len(google["result"]["dates"])):

            date = google["result"]["dates"][x]
            self.summary_frame['id'].append(x)
            self.summary_frame['date'].append(date)

            for metric in self.metrics:
                yandex_value = yandex["result"]["seriesByProjectsId"][str(self.project_id)][metric][x]
                yandex_value = str(yandex_value).replace('.', ',')
                self.summary_frame[f'yandex_{metric}'].append(yandex_value)

                google_value = google["result"]["seriesByProjectsId"][str(self.project_id)][metric][x]
                google_value = str(google_value).replace('.', ',')
                self.summary_frame[f'google_{metric}'].append(google_value)

            for top in self.tops:
                yandex_value = yandex["result"]["seriesByProjectsId"][str(self.project_id)]["tops"][top][x]
                self.summary_frame[f'yandex_{top}'].append(yandex_value)
                google_value = google["result"]["seriesByProjectsId"][str(self.project_id)]["tops"][top][x]
                self.summary_frame[f'google_{top}'].append(google_value)

        self.table = pd.DataFrame.from_dict(self.summary_frame, orient='index').transpose()

        return self.table


    def push_folders_summary_charts(self):

        self._get_folders_summary_charts()
        self._reformat_response_for_folders_summary_dataframe()
        df = self._reformat_response_for_folders_summary_dataframe()
        sheet_name = 'folders_summary_charts'

        sender = GoogleSheetWriter(self.service_file_path, self.work_book_id, sheet_name)
        sender.run(df)

def main():

    tv = Topvisor()
    tv.get_summary_chart()
    # tv.push_folders_summary_charts()


if __name__ == '__main__':

    main()
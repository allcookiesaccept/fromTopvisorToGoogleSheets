import json
import requests
import os
import datetime
import pandas as pd

class Topvisor:

    def __init__(self):

        # initializing and getting login variables
        self.user = ''
        self.key = ''
        self.project_id = ''


        with open('login_data.txt', 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            oauth = {}
            for line in lines:
                data = line.split(': ')
                oauth[data[0]] = data[1]
            self.user = oauth['user']
            self.key = oauth['key']
            self.project_id = oauth['project_id']
            file.close()

        # services urls
        self.sum_chart_url = '/v2/json/get/positions_2/summary_chart'
        self.keywords_url = '/v2/json/get/keywords_2/folders'


        print('Authorizing Topvisor')
        self.headers = {'Content-type': 'application/json', 'User-Id': self.user, 'Authorization': f'bearer {self.key}'}
        self.server = 'https://api.topvisor.com'
        self.date_today = str(datetime.date.today())
        self.region_index = {"yandex": 3, "google": 6}

        self.start = input('Please, enter start date "yyyy-mm-dd" : ')
        self.end = input('Please, enter second date "yyyy-mm-dd" or print "today": ')

        if self.end == 'today':
            self.end = self.date_today

        self.dates = [self.start, self.end]

    def _get_file_name(self, method):

        self.file_name = method.split('/')[-1]
        return self.file_name

    def get_folders(self):

        self._get_file_name(self.keywords_url)
        payload = {
            "project_id": self.project_id
        }
        response = requests.post(f'{self.server}{self.keywords_url}', headers=self.headers, data=json.dumps(payload))
        with open(f'{datetime.date.today()}_{self.file_name}.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()

    def get_projects(self):

        payload = {
            "show_site_stat": True,
            "show_searchers_and_regions": True
        }
        api_path = '/v2/json/get/projects_2/projects'
        response = requests.post(f'{self.server}{api_path}', headers=self.headers, data=json.dumps(payload))
        with open(f'topvisor_data/projects/projects-{datetime.date.today()}.json', "w", encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()
        if response:
            print(f'Data succesfully collected')
        return response.json()

    def get_summary_chart(self, search_engine: str):

        api_path = '/v2/json/get/positions_2/summary_chart'

        payload = {
            "project_id": 	self.project_id,
            "region_index": self.region_index[search_engine],
            "date1" : self.dates[0],
            "date2" : self.dates[-1],
            "type_range": 0,
            "show_visibility": True,
            "show_avg": True,
            "show_tops": True
        }

        response = requests.post(f'{self.server}{api_path}', headers=self.headers, data=json.dumps(payload))

        print(f'Requesting Topvisor - {search_engine}')
        if response.status_code == 200:
            print(f'Response successful')
        else:
            print(f'{str(response.status_code)} - Happens')

        with open(f'{datetime.date.today()}_{search_engine}_summary_chart.json', "w", encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()

        return response.json()

    def _get_summary_chart_all(self):

        api_path = '/v2/json/get/positions_2/summary_chart'
        region_index = {"yandex": 3, "google": 6}

        for key in region_index:
            payload = {
                "project_id": 	self.project_id,
                "region_index": region_index[key],
                "date1" : self.dates[0],
                "date2" : self.dates[-1],
                "type_range": 0,
                "show_visibility": True,
                "show_avg": True,
                "show_tops": True
            }

            response = requests.post(f'{self.server}{api_path}', headers=self.headers, data=json.dumps(payload))

            print(f'Requesting Topvisor - {key}')

            with open(f'{datetime.date.today()}_{key}_summary_chart.json', "w", encoding='utf-8') as file:
                json.dump(response.json(), file, indent=4, ensure_ascii=False)
                file.close()

    def _get_summary_chart_all_commercial(self):

        api_path = '/v2/json/get/positions_2/summary_chart'
        region_index = {"yandex": 3, "google": 6}

        for key in region_index:
            payload = {
                "project_id": self.project_id,
                "region_index": region_index[key],
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
                            "2"
                        ]
                    }
                ],
            }

            response = requests.post(f'{self.server}{api_path}', headers=self.headers, data=json.dumps(payload))

            print(f'Requesting Topvisor - {key} - commercial')

            with open(f'{datetime.date.today()}_{key}_commercial_summary_chart.json', "w", encoding='utf-8') as file:
                json.dump(response.json(), file, indent=4, ensure_ascii=False)
                file.close()

    def get_group_summary_chart(self, search_engine: str, group_folder_name: str, group_folder_id: int):

        api_path = '/v2/json/get/positions_2/summary_chart'

        payload = {
            "project_id": 	self.project_id,
            "region_index": self.region_index[search_engine],
            "date1" : self.dates[0],
            "date2" : self.dates[-1],
            "type_range": 0,
            "show_visibility": True,
            "show_avg": True,
            "show_tops": True,
            "filters": [
                {
                    "name": "group_folder_id",
                    "operator": "EQUALS",
                    "values": [
                        group_folder_id
                    ]
                }
            ],
            "group_folder_id_depth": "1"
        }

        response = requests.post(f'{self.server}{api_path}', headers=self.headers, data=json.dumps(payload))

        print(f'Requesting Topvisor - {search_engine}: {group_folder_name}')


        with open(f'folders/{datetime.date.today()}_{search_engine}_{group_folder_name}_summary_chart_.json', "w",
                  encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()

        return response.json()


    def _create_summary_google_doc(self):

        workbook_id = '10bQ3R1LvWd3QQW55ALaNOtdxLrZWdrz57Uhrhnu1bRw'
        secret = 'D:\\pyprojects\\datastudio\\pysheets-347309-9629095400b4.json'
        sheet_name = 'summary'

        self._get_summary_chart_all()
        self._get_summary_chart_all_commercial()
        self._create_summary_table()
        sender = OlapChannels(secret,workbook_id, sheet_name)

        sender.run(self.summary_result)

    def _create_summary_table(self):

        google = pd.read_json(f'D:\\pyprojects\\datastudio\\topvisor\\{self.date_today}_google_summary_chart.json')
        google_com = pd.read_json(f'D:\\pyprojects\\datastudio\\topvisor\\{self.date_today}_google_commercial_summary_chart.json')
        yandex = pd.read_json(f'D:\\pyprojects\\datastudio\\topvisor\\{self.date_today}_yandex_summary_chart.json')
        yandex_com = pd.read_json(f'D:\\pyprojects\\datastudio\\topvisor\\{self.date_today}_yandex_commercial_summary_chart.json')

        self.summary_result = {}

        for x in range(len(google["result"]["dates"])):
            day = {}
            date = google["result"]["dates"][x]
            day['date'] = date
            g_avg = google["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            day['g_avg'] = str(g_avg).replace('.', ',')
            g_vis = google["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['g_vis'] = str(g_vis).replace('.', ',')
            y_avg = yandex["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            day['y_avg'] = str(y_avg).replace('.', ',')
            y_vis_com = yandex["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['y_vis'] = str(y_vis_com).replace('.', ',')
            g_avg_com = google_com["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            day['g_avg_com'] = str(g_avg_com).replace('.', ',')
            g_vis_com = google_com["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['g_vis_com'] = str(g_vis_com).replace('.', ',')
            y_avg_com = yandex_com["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            day['y_avg_com'] = str(y_avg_com).replace('.', ',')
            y_vis_com = yandex_com["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['y_vis_com'] = str(y_vis_com).replace('.', ',')

            self.summary_result[date] = day
            
        self.summary_result = pd.DataFrame(self.summary_result).transpose()
        print(self.summary_result)
        return self.summary_result

    def get_folders_summary_chart(self):

        api_path = '/v2/json/get/positions_2/summary_chart'

        region_index = {"yandex": 3, "google": 6}

        folders = {"iphone": 861539, "ipad": 861590, "mac": 861565, "watch": 861584}

        for key in region_index:
            for folder in folders:

                payload = {
                    "project_id": 	self.project_id,
                    "region_index": region_index[key],
                    "date1" : self.dates[0],
                    "date2" : self.dates[-1],
                    "type_range": 0,
                    "show_visibility": True,
                    "show_avg": True,
                    "show_tops": True,
                    "filters": [
                        {
                            "name": "group_folder_id",
                            "operator": "EQUALS",
                            "values": [
                                folders[folder]
                            ]
                        }
                    ],
                    "group_folder_id_depth": "1"
                }

                response = requests.post(f'{self.server}{api_path}', headers=self.headers, data=json.dumps(payload))

                print(f'Requesting Topvisor - {key}: {folder}')


                with open(f'folders/{datetime.date.today()}_{key}_{folder}_summary_chart.json', "w",
                          encoding='utf-8') as file:
                    json.dump(response.json(), file, indent=4, ensure_ascii=False)
                    file.close()

    def _create_yandex_folders_table(self):

        self.yandex_folders = {}
        iphone = pd.read_json(f'D:\\pyprojects\\datastudio\\topvisor\\folders\\{self.date_today}_yandex_iphone_summary_chart_.json')
        mac = pd.read_json(f'D:\\pyprojects\\datastudio\\topvisor\\folders\\{self.date_today}_yandex_mac_summary_chart.json')
        watch = pd.read_json(f'D:\\pyprojects\\datastudio\\topvisor\\folders\\{self.date_today}_yandex_watch_summary_chart.json')
        ipad = pd.read_json(f'D:\\pyprojects\\datastudio\\topvisor\\folders\\{self.date_today}_yandex_ipad_summary_chart.json')

        for x in range(len(iphone["result"]["dates"])):
            day = {}
            date = iphone["result"]["dates"][x]
            day['date'] = date
            iphone_avg = iphone["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            iphone_vis = iphone["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['iphone_avg'], day['iphone_vis'] = iphone_avg, iphone_vis
            mac_avg = mac["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            mac_vis = mac["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['mac_avg'], day['mac_vis'] = mac_avg, mac_vis
            ipad_avg = ipad["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            ipad_vis = ipad["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['ipad_avg'], day['iphone_vis'] = ipad_avg, ipad_vis
            watch_avg = watch["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            watch_vis = watch["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['watch_avg'], day['watch_vis'] = watch_avg, watch_vis

            self.yandex_folders[date] = day
        self.yandex_folders = pd.DataFrame(self.yandex_folders).transpose()
        return self.yandex_folders

    def _create_google_folders_table(self):

        self.google_folders = {}
        iphone = pd.read_json(
            f'D:\\pyprojects\\datastudio\\topvisor\\folders\\{self.date_today}_google_iphone_summary_chart.json')
        mac = pd.read_json(
            f'D:\\pyprojects\\datastudio\\topvisor\\folders\\{self.date_today}_google_mac_summary_chart.json')
        watch = pd.read_json(
            f'D:\\pyprojects\\datastudio\\topvisor\\folders\\{self.date_today}_google_watch_summary_chart.json')
        ipad = pd.read_json(
            f'D:\\pyprojects\\datastudio\\topvisor\\folders\\{self.date_today}_google_ipad_summary_chart.json')

        for x in range(len(iphone["result"]["dates"])):
            day = {}
            date = iphone["result"]["dates"][x]
            day['date'] = date
            iphone_avg = iphone["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            iphone_vis = iphone["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['iphone_avg'], day['iphone_vis'] = iphone_avg, iphone_vis
            mac_avg = mac["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            mac_vis = mac["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['mac_avg'], day['mac_vis'] = mac_avg, mac_vis
            ipad_avg = ipad["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            ipad_vis = ipad["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['ipad_avg'], day['iphone_vis'] = ipad_avg, ipad_vis
            watch_avg = watch["result"]["seriesByProjectsId"]["4944800"]["avg"][x]
            watch_vis = watch["result"]["seriesByProjectsId"]["4944800"]["visibility"][x]
            day['watch_avg'], day['watch_vis'] = watch_avg, watch_vis

            self.google_folders[date] = day

        self.google_folders = pd.DataFrame(self.google_folders).transpose()

        return self.google_folders

    def _create_summary_by_folders_google_doc(self):

        workbook_id = '10bQ3R1LvWd3QQW55ALaNOtdxLrZWdrz57Uhrhnu1bRw'
        secret = 'D:\\pyprojects\\datastudio\\pysheets-347309-9629095400b4.json'

        self.get_folders_summary_chart()
        self._create_yandex_folders_table()
        sheet_name = 'yandex_folders'
        sender = OlapChannels(secret,workbook_id, sheet_name)
        sender.run(self.yandex_folders)
        self._create_google_folders_table()
        sheet_name = 'google_folders'
        sender = OlapChannels(secret,workbook_id, sheet_name)
        sender.run(self.google_folders)



if __name__ == '__main__':

    tv = Topvisor()
    # tv._create_summary_google_doc()
    # tv._get_summary_chart_all_commercial()
    tv._create_summary_by_folders_google_doc()
    #
from datetime import datetime, timedelta
from config.settings import Config
from typing import List, Dict

class ProjectManager:
    def __init__(self, config: Config):
        self.config: Config = config
        self.topvisor = self._initialize_topvisor()


    def _initialize_topvisor(self):
        """
        Initialize the Topvisor client using the configuration.
        :return: Topvisor API client instance.
        """
        from pytopvisor.topvisor import Topvisor

        user_id = self.config.get("user_id")
        api_key = self.config.get("api_key")

        if not user_id or not api_key:
            raise ValueError("Missing 'user_id' or 'api_key' in configuration.")

        return Topvisor(user_id=user_id, api_key=api_key)


    def get_dates_from_history(self, project_id: int, region_index: int, days_back: int = 3) -> List[str]:
        """
        Get dates from the history of position checks.
        :param project_id: ID of the project.
        :param region_index: Index of the region.
        :param days_back: Number of days to look back.
        :return: List of dates as strings.
        """
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        print(start_date, end_date)

        history = self.topvisor.run_task(
            "get_history",
            project_id=project_id,
            regions_indexes=[region_index],
            date1=start_date,
            date2=end_date,
            show_exists_dates=True
        )
        # Extract all dates from the response
        all_dates = history["result"]["existsDates"]

        # Filter the last 3 dates (or any other number)
        last_3_dates = sorted(
            all_dates,
            key=lambda x: datetime.strptime(x, "%Y-%m-%d"),
            reverse=True
        )[:3]

        return last_3_dates

    def get_summary_data(self, project_id: int, region_index: int, dates: List[str]) -> List[Dict]:
        """
        Get summary data for the given dates.
        :param project_id: ID of the project.
        :param region_index: Index of the region.
        :param dates: List of dates to retrieve data for.
        :return: List of dictionaries containing summary data.
        """
        summary_chart = self.topvisor.run_task(
            "get_summary_chart",
            project_id=project_id,
            region_index=region_index,
            dates=dates,
            show_tops=True,
            show_avg=True,
            show_visibility=True
        )

        result = []
        for i, date in enumerate(summary_chart["result"]["dates"]):
            data = {
                "date": date,
                "project_id": project_id,
                "region_index": region_index,
                "all": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["all"][i],
                "top_1_3": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["1_3"][i],
                "top_1_10": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["1_10"][i],
                "top_11_30": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["11_30"][i],
                "top_31_50": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["31_50"][i],
                "top_51_100": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["51_100"][i],
                "avg_position": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["avg"][i],
                "visibility": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["visibility"][i]
            }
            result.append(data)
        return result

    def process_project(self, project_id: int, region_index: int, days_back: int = 3) -> List[Dict]:
        """
        Process a single project and return the formatted data.
        :param project_id: ID of the project.
        :param region_index: Index of the region.
        :param days_back: Number of days to look back.
        :return: List of dictionaries containing processed data.
        """
        # Step 1: Get dates from history
        dates = self.get_dates_from_history(project_id, region_index, days_back)

        # Step 2: Get summary data for the dates
        summary_data = self.get_summary_data(project_id, region_index, dates)

        return summary_data

    def run(self, days_back: int = 3) -> List[Dict]:
        """
        Run the entire process for all projects and return the combined data.
        :param days_back: Number of days to look back.
        :return: List of dictionaries containing processed data for all projects.
        """
        all_data = []

        for project in self.config.get("projects", []):
            project_id = project.get("project_id")
            region_index = project.get("region_index")

            if not project_id or not region_index:
                raise ValueError("Each project must have 'project_id' and 'region_index'")

            project_data = self.process_project(project_id, region_index, days_back)
            all_data.extend(project_data)

        return all_data
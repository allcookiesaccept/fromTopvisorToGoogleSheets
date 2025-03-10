from datetime import datetime, timedelta
from config.settings import Config
from typing import List, Dict
from config.logger import logger
from db.sqlitedb import SQLiteDB
from db.googlesheetwriter import GoogleSheetsManager

class ProjectManager:

    def __init__(self, config: Config):
        logger.debug("Initializing ProjectManager...")
        self.config: Config = config
        self.topvisor = self._initialize_topvisor()
        self.db = SQLiteDB()
        self.google_sheets = self._initialize_google_sheets()
        logger.info("ProjectManager initialized successfully.")

    def _initialize_topvisor(self):
        """
        Initialize the Topvisor client using the configuration.
        :return: Topvisor API client instance.
        """
        from pytopvisor.topvisor import Topvisor
        logger.debug("Initializing Topvisor...")

        user_id = self.config.get("user_id")
        api_key = self.config.get("api_key")

        if not user_id or not api_key:
            raise ValueError("Missing 'user_id' or 'api_key' in configuration.")

        logger.info("Topvisor initialized successfully.")
        return Topvisor(user_id=user_id, api_key=api_key)

    def _initialize_google_sheets(self):
        """
        Initialize the Google Sheets Manager.
        :return: GoogleSheetsManager instance.
        """
        service_file_name = self.config.get("service_file")
        spreadsheet_id = self.config.get("google_sheets")

        if not service_file_name or not spreadsheet_id:
            raise ValueError("Missing 'service_file' or 'google_sheets' in configuration.")

        return GoogleSheetsManager(
            credentials_path=f"config/{service_file_name}",
            spreadsheet_id=spreadsheet_id
        )


    def get_dates_from_history(self, project_id: int, region_index: int, days_back: int = 3) -> List[str]:
        """
        Get dates from the history of position checks.
        :param project_id: ID of the project.
        :param region_index: Index of the region.
        :param days_back: Number of days to look back.
        :return: List of dates as strings.
        """
        logger.debug(f"Fetching dates from history for project_id={project_id}, region_index={region_index}, days_back={days_back}")
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        logger.debug(f"Start date: {start_date}, End date: {end_date}")

        try:
            history = self.topvisor.run_task(
                "get_history",
                project_id=project_id,
                regions_indexes=[region_index],
                date1=start_date,
                date2=end_date,
                show_exists_dates=True
            )
            logger.debug(f"Get History response: {history}")

            # Extract all dates from the response
            all_dates = history["result"]["existsDates"]

            # Filter the last 3 dates (or any other number)
            last_3_dates = sorted(
                all_dates,
                key=lambda x: datetime.strptime(x, "%Y-%m-%d"),
                reverse=True
            )[:3]
            logger.info(f"Last 3 dates fetched: {last_3_dates}")

            return last_3_dates

        except KeyError as e:
            logger.error(f"KeyError in get_dates_from_history: {e}")
            raise ValueError(f"Unexpected API response format. Missing key: {e}")
        except Exception as e:
            logger.error(f"Error fetching dates from history: {e}")
            raise

    def get_summary_data(self, project_id: int, region_index: int, dates: List[str]) -> List[Dict]:
        """
        Get summary data for the given dates.
        :param project_id: ID of the project.
        :param region_index: Index of the region.
        :param dates: List of dates to retrieve data for.
        :return: List of dictionaries containing summary data.
        """
        logger.debug(f"Fetching summary data for project_id={project_id}, region_index={region_index}, dates={dates}")

        try:
            summary_chart = self.topvisor.run_task(
                "get_summary_chart",
                project_id=project_id,
                region_index=region_index,
                dates=dates,
                show_tops=True,
                show_avg=True,
                show_visibility=True
            )
            logger.debug(f"Summary chart response: {summary_chart}")

            result = []
            for i, date in enumerate(summary_chart["result"]["dates"]):
                data = {
                    "date": date,
                    "project_id": project_id,
                    "region_index": region_index,
                    "all_positions": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["all"][i],
                    "top_1_3": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["1_3"][i],
                    "top_1_10": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["1_10"][i],
                    "top_11_30": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["11_30"][i],
                    "top_31_50": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["31_50"][i],
                    "top_51_100": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["tops"]["51_100"][i],
                    "avg_position": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["avg"][i],
                    "visibility": summary_chart["result"]["seriesByProjectsId"][str(project_id)]["visibility"][i]
                }
                result.append(data)

            logger.info(f"Summary data processed for {len(result)} dates.")
            return result

        except KeyError as e:
            logger.error(f"KeyError in get_summary_data: {e}")
            raise ValueError(f"Unexpected API response format. Missing key: {e}")
        except Exception as e:
            logger.error(f"Error fetching summary data: {e}")
            raise

    def process_project(self, project_id: int, region_index: int, days_back: int = 3) -> List[Dict]:
        """
        Process a single project and return the formatted data.
        :param project_id: ID of the project.
        :param region_index: Index of the region.
        :param days_back: Number of days to look back.
        :return: List of dictionaries containing processed data.
        """
        logger.info(f"Processing project_id={project_id}, region_index={region_index}")

        # Step 1: Get dates from history
        dates = self.get_dates_from_history(project_id, region_index, days_back)

        # Step 2: Get summary data for the dates
        summary_data = self.get_summary_data(project_id, region_index, dates)

        # Step 3: Save data to the database
        self.save_to_db(summary_data)

        return summary_data

    def run(self, days_back: int = 3) -> List[Dict]:
        """
        Run the entire process for all projects and return the combined data.
        :param days_back: Number of days to look back.
        :return: List of dictionaries containing processed data for all projects.
        """
        logger.info(f"Starting the process with days_back={days_back}...")

        all_data = []

        for project in self.config.get("projects", []):
            project_id = project.get("project_id")
            region_index = project.get("region_index")

            if not project_id or not region_index:
                logger.error("Each project must have 'project_id' and 'region_index'")
                raise ValueError("Each project must have 'project_id' and 'region_index'")

            logger.info(f"Processing project_id={project_id}, region_index={region_index}")

            project_data = self.process_project(project_id, region_index, days_back)
            all_data.extend(project_data)

        logger.info(f"Process completed. Total records processed: {len(all_data)}")
        self.copy_to_google_sheets()
        logger.info(f"Google Sheets updated")
        return all_data

    def save_to_db(self, data: List[Dict]):
        """
        Save data to the SQLite database and then copy it to Google Sheets.
        :param data: List of dictionaries containing data to save.
        """
        for record in data:
            if not self.db.record_exists("project_data", record["date"], record["project_id"], record["region_index"]):
                self.db.create("project_data", record)
            else:
                logger.debug(f"Record for date={record['date']}, project_id={record['project_id']}, region_index={record['region_index']} already exists. Skipping.")
        logger.info("Data saved to SQLite successfully.")

        # Copy data from SQLite to Google Sheets

    def copy_to_google_sheets(self):
        """
        Copy all data from SQLite to Google Sheets.
        """
        logger.info("Copying data from SQLite to Google Sheets...")

        # Read all data from SQLite
        sqlite_data = self.db.read("project_data")

        # Transform data into a list of rows for Google Sheets
        rows = [
            [
                record["date"],
                record["project_id"],
                record["region_index"],
                record["all_positions"],
                record["top_1_3"],
                record["top_1_10"],
                record["top_11_30"],
                record["top_31_50"],
                record["top_51_100"],
                record["avg_position"],
                record["visibility"]
            ]
            for record in sqlite_data
        ]

        # Add header row
        header = [
            "Date",
            "Project ID",
            "Region Index",
            "All Positions",
            "Top 1-3",
            "Top 1-10",
            "Top 11-30",
            "Top 31-50",
            "Top 51-100",
            "Avg Position",
            "Visibility"
        ]
        rows.insert(0, header)

        # Write data to Google Sheets
        self.google_sheets.write("Sheet1", "A1", rows)
        logger.info("Data copied to Google Sheets successfully.")


if __name__ == "__main__":
    from config.settings import Config

    config = Config()

    pm = ProjectManager(config)
    pm.run()
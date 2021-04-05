
import configparser
import json
from summary.summary import *
from summary.summary_container import SummaryContainer
from connector import oura_api_connector, gui_input_connector, csv_storage_connector
from common.date_helper import *
from common.constants import *
from storage.csv_storage import CsvStorage
from analyser import abstract_analyser, plotly_analyser


if __name__ == '__main__':

            
    config = configparser.ConfigParser()
    config.read("config.ini")
    access_token = config["oura.auth"].get('access-token')

    subj_conf = config['subective.summary.data']
    subjective_tracking_items = list(subj_conf.items())

    storage_file_name = config['storage.filename'].get('filename')
    storage_file_path = ["quantified_self_dashboard", "data", storage_file_name]

    output_location = ["output"]

    conn_oura = oura_api_connector.OuraApiConnector(access_token)
    conn_sub = gui_input_connector.GuiInputConnector(subjective_tracking_items)
    conn_storage = csv_storage_connector.CsvStorageConnector(storage_file_path)
    connectors = [conn_storage, conn_oura, conn_sub]

    start, end = "2021-03-01", "2021-04-03"

    container = SummaryContainer(containing_sleep=True, containing_readiness=True, containing_activity=True, containing_bedtime=True)
    container.load(connectors, get_day_before(start), end)

    storage = CsvStorage(storage_file_path)
    storage.save(container)

    analyser = plotly_analyser.PlotlyAnalyser(output_location, container)
    analyser.analyse(start, end, AnalysisType.sleep_score_distribution)
    analyser.analyse(start, end, AnalysisType.readiness_score_distribution)
    analyser.analyse(start, end, AnalysisType.activity_score_distribution)
    analyser.analyse(start, end, AnalysisType.scores_daily)
    analyser.analyse(start, end, AnalysisType.bedtimes_daily)
    analyser.analyse(start, end, AnalysisType.sleep_durations)
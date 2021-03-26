
import configparser
import json
from summary.summary import *
from summary.summary_container import SummaryContainer
from connector import oura_api_connector, gui_input_connector, csv_storage_connector
from common.date_helper import *
from storage.csv_storage import CsvStorage
from analyser import abstract_analyser, plotly_analyzer


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

    container = SummaryContainer(containing_subjective=False)
    container.load(connectors, "2021-03-01", "2021-03-20")

    # storage = CsvStorage(storage_file_path)
    # storage.save(container)

    analyser = plotly_analyzer.PlotlyAnalyzer(output_location, container)
    analyser.analyze("2021-03-01", "2021-03-20", PERIODICITY_DAILY, "test")
    print()
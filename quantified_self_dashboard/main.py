
import configparser
import json
from summary.summary import *
from summary.summary_container import SummaryContainer
from connector import oura_api_connector, gui_input_connector
from common.date_helper import *
from storage.storage import CsvStorage


from ast import literal_eval

if __name__ == '__main__':

            
    config = configparser.ConfigParser()
    config.read("config.ini")
    access_token = config["oura.auth"].get('access-token')

    subj_conf = config['subective.summary.data']
    subjective_tracking_items = list(subj_conf.items())

    conn_oura = oura_api_connector.OuraApiConnector(access_token)
    conn_sub = gui_input_connector.GuiInputConnector(subjective_tracking_items)
    connectors = [conn_oura, conn_sub]

    container = SummaryContainer(containing_subjective=True)
    container.load(connectors, "2021-03-01", "2021-03-22")

    storage = CsvStorage(["quantified_self_dashboard", "data", "testfile.csv"])
    storage.save(container)
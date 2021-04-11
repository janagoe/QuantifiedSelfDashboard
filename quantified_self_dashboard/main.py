
import configparser
import json
from summary.summary import *
from summary.summary_container import SummaryContainer
from connector import oura_api_connector, gui_input_connector, csv_storage_connector
from common.date_helper import *
from common.constants import *
from storage.csv_storage import CsvStorage
from analyser import abstract_analyser, plotly_analyser
import pandas as pd

import wx

from ui.main_frame import MainFrame


class SubjectiveInputCallbackWrapper:
    
    def __init__(self, gui_input_connector, summary_container, storage, subjective_input_structure):
        self.__gui_intput_connector = gui_input_connector
        self.__summary_container = summary_container
        self.__storage = storage
        self.__subjective_input_structure = subjective_input_structure

        self.__load_missing_subjective_data_days()

    def __load_missing_subjective_data_days(self):
        # TODO loading from 
        self.__missing_subjective_data_days = ["2021-03-01", "2021-03-15", "2021-04-01", "2021-05-01", "2021-05-31"]
    
    def get_missing_subjective_data_days(self):
        return self.__missing_subjective_data_days 

    def get_subjective_input_structure(self):
        return self.__subjective_input_structure

    def get_number_of_needed_dynamic_input_rows(self):
        return len(self.__subjective_input_structure)

    def add_subjective_input(self, summary_date, data: dict):
        print("add_subjective_input", summary_date, data)
        self.__gui_intput_connector.add_subjective_input(summary_date, data)

    def save():
        # TODO save into storage
        print("save")


    





if __name__ == "__main__":

    # TODO: improve config structure
    config = configparser.ConfigParser()
    config.read("config.ini")
    access_token = config["oura.auth"].get('access-token')

    subj_conf = config['subective.summary.data']
    # subjective_input_structure = list(subj_conf.items())

    # TODO check config subjective input
    # transform into constants
    subjective_input_structure = [('a', SubjectiveMeasurementType.bool), ('b', SubjectiveMeasurementType.number), ('c', SubjectiveMeasurementType.percentage)]

    storage_file_name = config['storage.filename'].get('filename')
    storage_file_path = ["quantified_self_dashboard", "data", storage_file_name]

    output_location = ["output"]

    conn_oura = oura_api_connector.OuraApiConnector(access_token)
    conn_sub = gui_input_connector.GuiInputConnector(subjective_input_structure)
    conn_storage = csv_storage_connector.CsvStorageConnector(storage_file_path)

    container = SummaryContainer(containing_sleep=True, containing_readiness=True, containing_activity=True, containing_bedtime=True, containing_subjective=True)

    
    # preloading everything from the storage connector
    # container.load()
    # TODO option loading everything

    storage = CsvStorage(storage_file_path)
    analyser = plotly_analyser.PlotlyAnalyser(output_location, container)


    subjective_input_callback_wrapper = SubjectiveInputCallbackWrapper(conn_sub, container, storage, subjective_input_structure)

    app = wx.App()
    m = MainFrame(subjective_input_callback_wrapper)
    m.Show()
    app.MainLoop()

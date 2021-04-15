
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
from ui.callback_wrappers import *




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

    # TODO get through config
    starting_date = "2021-03-01"

    conn_oura = oura_api_connector.OuraApiConnector(access_token)
    conn_sub = gui_input_connector.GuiInputConnector(subjective_input_structure)
    conn_storage = csv_storage_connector.CsvStorageConnector(storage_file_path)

    container = SummaryContainer(starting_date, containing_sleep=True, containing_readiness=True, containing_activity=True, containing_bedtime=True, containing_subjective=True)
    container.add_storage_connector(conn_storage)
    container.add_api_connector(conn_oura)
    container.add_user_connector(conn_sub)

    container.preload()
    container.load()

    storage = CsvStorage(storage_file_path)
    analyser = plotly_analyser.PlotlyAnalyser(output_location, container)

    subjective_input_callback_wrapper = SubjectiveInputCallbackWrapper(conn_sub, container, storage, subjective_input_structure, analyser)
    main_tab_callback_wrapper = MainTabCallbackWrapper(container, storage)
    analysis_tab_callbak_wrapperr = AnalysisTabCallbackWrapper(analyser, starting_date)

    app = wx.App()
    m = MainFrame(subjective_input_callback_wrapper, main_tab_callback_wrapper, analysis_tab_callbak_wrapperr)
    m.Show()
    app.MainLoop()

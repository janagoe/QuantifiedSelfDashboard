from typing import List
from common.constants import *
from common.date_helper import *
from datetime import datetime


class MainTabCallbackWrapper:
    def __init__(self, summary_container, storage):
        self.__summary_container = summary_container
        self.__storage = storage

    def save_session(self):
        self.__summary_container.load()
        self.__storage.save(self.__summary_container)
        print("finished saving")




class AnalysisTabCallbackWrapper:
    def __init__(self, analyser, starting_date):
        self.__analyser = analyser
        self.__starting_date = starting_date

    def get_available_dates(self) -> List[str]:
        return all_date_strings_between_dates(self.__starting_date, datetime_to_simple_iso(datetime.today()))

    def get_analysis_type_choice_list(self) -> List[str]:
        return list(map(lambda x: x.name, all_analysis_types))

    def create_analysis(self, start, end):
        analysis_type = AnalysisType[selection]
        # self.__analyser.analyse()

    def get_starting_date(self):
        return self.__starting_date



class SubjectiveInputCallbackWrapper:
    
    def __init__(self, gui_input_connector, summary_container, storage, subjective_input_structure, analyser):
        self.__gui_intput_connector = gui_input_connector
        self.__summary_container = summary_container
        self.__storage = storage
        self.__analyser = analyser
        self.__subjective_input_structure = subjective_input_structure

        self.__load_missing_subjective_data_days()

    def __load_missing_subjective_data_days(self):
        self.__missing_subjective_data_days = self.__summary_container.get_missing_subjective_data_days()
    
    def get_missing_subjective_data_days(self):
        return self.__missing_subjective_data_days 

    def get_subjective_input_structure(self):
        return self.__subjective_input_structure

    def get_number_of_needed_dynamic_input_rows(self):
        return len(self.__subjective_input_structure)

    def add_subjective_input(self, summary_date, data: dict):
        self.__gui_intput_connector.add_subjective_input(summary_date, data)

    

import random 
from typing import Tuple, List, Union

from common.constants import SummaryType, SubjectiveMeasurementType, SUMMARY_DATE
from connector.abstract_connector import AbstractConnector
from summary.summary import Subjective


class GuiInputConnector(AbstractConnector):

    supported_summary_types = [SummaryType.subjective]

    def __init__(self, subjective_tracking_items: List[Tuple[str, str]]):
        # TODO: reconsider this


        self.__input_data_sets = dict()

        self.__subjective_tracking_attr_types = dict()
        self.__subjective_tracking_attributes = []
        for attr_name, attr_type in subjective_tracking_items:

            # must be a valid type
            if attr_type in Subjective.subjective_tracking_types:
                self.__subjective_tracking_attributes.append(attr_name)
                self.__subjective_tracking_attr_types[attr_name] = attr_type
            else:
                raise ValueError("Invalid Subjective Tracking Type")
            
        # no duplication of attribute names
        if len(self.__subjective_tracking_attr_types) != len(self.__subjective_tracking_attributes):
            raise ValueError("Duplication of Subjective Tracking Names")

    def get_summary_data(self, summary_type: SummaryType, date: str) -> Tuple[bool, dict]:

        if summary_type != SummaryType.subjective:
            raise AttributeError("The GuiInputConnector can only collect Subjective Summary Types")

        if date in self.__input_data_sets.keys():
            data = self.__input_data_sets[date]
            return True, data

        return False, dict()


    def add_subjective_input(self, summary_date: str, input_data: dict()):
        # TODO: add checks
        input_data[SUMMARY_DATE] = summary_date
        self.__input_data_sets[summary_date] = input_data
   
    def preload(self, **kwargs):
        # preloading process is passively done through the gui
        pass

    def get_earliest_and_latest_vailable_summary_date(self) -> Tuple[Union[str, None], Union[str, None]]:
        available_dates = self.__input_data_sets.keys()

        earliest = min(available_dates)
        latest = max(available_dates)

        return earliest, latest
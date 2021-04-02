import random 
from typing import Tuple, List

from common.constants import SummaryType, SubjectiveMeasurementType, SUMMARY_DATE
from connector.abstract_connector import AbstractConnector
from summary.summary import Subjective



class GuiInputConnector(AbstractConnector):

    supported_summary_types = [SummaryType.subjective]

    def __init__(self, subjective_tracking_items: List[Tuple[str, str]]):

        self.__subjective_tracking_attr_types = dict()
        self.__subjective_tracking_attributes = []
        for attr_name, attr_type_str in subjective_tracking_items:

            attr_type = SubjectiveMeasurementType[attr_type_str]

            # must be a valid type
            if attr_type in Subjective.subjective_tracking_types:
                self.__subjective_tracking_attributes.append(attr_name)
                self.__subjective_tracking_attr_types[attr_name] = attr_type
            else:
                raise ValueError("Invalid Subjective Tracking Type")
            
        # no duplication of attribute names
        if len(self.__subjective_tracking_attr_types) != len(self.__subjective_tracking_attributes):
            raise ValueError("Duplication of Subjective Tracking Names")

    def get_summary(self, summary_type: SummaryType, date: str) -> Tuple[bool, dict]:

        if summary_type != SummaryType.subjective:
            raise AttributeError("The GuiInputConnector can only collect Subjective Summary Types")

        data = self.__ask_data_from_user()
        data[SUMMARY_DATE] = date
        
        return True, data

    def __ask_data_from_user(self):
        """
        Creating dummy data for now.
        Later getting the data from a gui
        """

        data = dict()
        for attr in self.__subjective_tracking_attributes:
            attr_type = self.__subjective_tracking_attr_types[attr]
            if attr_type == SubjectiveMeasurementType.bool:
                value = random.choice([True, False])
            elif attr_type == SubjectiveMeasurementType.number:
                value = random.randrange(1000) - 500
            elif attr_type == SubjectiveMeasurementType.percentage:
                value = random.randrange(101)
            data[attr] = value

        return data

   
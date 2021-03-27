import random 
from typing import Tuple, List
from common.constants import *
from connector.abstract_connector import AbstractConnector
from summary.summary import Subjective



class GuiInputConnector(AbstractConnector):

    supported_summary_types = [SUBJECTIVE]

    def __init__(self, subjective_tracking_items: List[Tuple[str, str]]):

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

    def get_summary(self, summary_type: str, date: str) -> Tuple[bool, dict]:

        if summary_type != SUBJECTIVE:
            raise AttributeError("The GuiInputConnector can only collect Subjective Summary Types")

        data = self.__ask_data_from_user()
        data['summary_date'] = date
        
        return True, data

    def __ask_data_from_user(self):
        """
        Creating dummy data for now.
        Later getting the data from a gui
        """

        data = dict()
        for attr in self.__subjective_tracking_attributes:
            attr_type = self.__subjective_tracking_attr_types[attr]
            if attr_type == TYPE_BOOL:
                value = random.choice([True, False])
            elif attr_type == TYPE_NUMBER:
                value = random.randrange(1000) - 500
            elif attr_type == TYPE_PERCENTAGE:
                value = random.randrange(101)
            data[attr] = value

        return data

   
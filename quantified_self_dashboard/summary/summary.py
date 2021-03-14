from connector.abstract_connector import AbstractConnector
from common.constants import *
import requests


class Summary:
    """
    Base class for summaries of one given day.
    After loading the data, all values are stored as class attributes. 
    """

    def __init__(self, summary_type='undefined'):
        self._summary_type = summary_type

    def _parse_connector_response(self, day_data: dict) -> None:
        """
        Parsing the data of the day by dynamically creating
        class attributes, named after the dictionary key. 
        """

        for var_name, var_value in day_data.items():
            setattr(self, var_name, var_value)

    def load(self, connector: AbstractConnector, date: str) -> bool:
        """
        Requesting the data for the given date via the connector,
        parsing it and creating variables. 
        Each Summary Object only contains data for one day. Therefore
        we only need to retrieve data for this given day. 
        """
        
        success, resp_dict = connector.get_summary(self._summary_type, date)
        
        if success:
            self._parse_connector_response(resp_dict)

        return success

    def __str__(self):
        return "Summary (Type: {}, Date: {})".format(self.summary_type, self.summary_date)

    @property
    def summary_type(self):
        return self._summary_type

    @property
    def summary_date(self):
        return self._summary_date

    @summary_date.setter
    def summary_date(self, summary_date: str):
        self._summary_date = summary_date


class Sleep(Summary):
    def __init__(self):
        super().__init__(summary_type=SLEEP)


class Readiness(Summary):
    def __init__(self):
        super().__init__(summary_type=READINESS)


class Activity(Summary):
    def __init__(self):
        super().__init__(summary_type=ACTIVITY)


class Bedtime(Summary):

    def __init__(self):
        super().__init__(summary_type=BEDTIME)


class Subjective(Summary):

    def __init__(self):
        super().__init__(summary_type=SUBJECTIVE)



def get_summary_class_from_str(summary_type):
    
    str_to_class = {
        SLEEP: Sleep,
        READINESS: Readiness,
        ACTIVITY: Activity,
        BEDTIME: Bedtime,
        SUBJECTIVE: Subjective
    }

    return str_to_class[summary_type]
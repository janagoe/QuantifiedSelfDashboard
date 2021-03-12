from oura_api_connector import OuraApiConnector
from constants import *



class Summary:
    """
    Base class for summaries of one given day.
    After loading the data, all values are stored as class attributes. 
    """

    def __init__(self, summary_type='undefined'):
        self._summary_type = summary_type

    def _parse_day(self, day_data: dict):
        """
        Parsing the data of the day by dynamically creating
        class attributes, named after the dictionary key. 
        """

        for var_name, var_value in day_data.items():
            setattr(self, var_name, var_value)

    def load(self, connector: OuraApiConnector, date: str):
        """
        Requesting the data for the given date via the connector,
        parsing it and creating variables. 

        Each Summary Object only contains data for one day. Therefore
        we only need to retrieve data for this given day. 
        """
        
        response = connector.get_summary(self._summary_type, start=date, end=date)
        day_data = response[self._summary_type][0]
        self._parse_day(day_data)

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

    def load(self, connector: OuraApiConnector, date: str):
        """
        The API response of Bedtime varies slightly from the other summary types. 
        Also before parsing, we rename the dictionary key 'date' to 'summary_date'
        to make the attributes consistent with the other classes.
        """
        
        response = connector.get_summary(self._summary_type, start=date, end=date)
        
        day_data = response['ideal_bedtimes'][0]
        day_data['summary_date'] = day_data.pop('date')
        
        self._parse_day(day_data)

    
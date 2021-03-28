from connector.abstract_connector import AbstractConnector
from common.constants import SummaryType, SUMMARY_DATE


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
        self.__measurement_attributes = []
        for var_name, var_value in day_data.items():
            setattr(self, var_name, var_value)
            self.__measurement_attributes.append(var_name)

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

    @property
    def measurement_attributes(self):
        return self.__measurement_attributes


class Sleep(Summary):
    def __init__(self):
        super().__init__(summary_type=SummaryType.sleep)


class Readiness(Summary):
    def __init__(self):
        super().__init__(summary_type=SummaryType.readiness)


class Activity(Summary):
    def __init__(self):
        super().__init__(summary_type=SummaryType.activity)


class Bedtime(Summary):

    def __init__(self):
        super().__init__(summary_type=SummaryType.bedtime)


class Subjective(Summary):

    subjective_tracking_types = [TYPE_BOOL, TYPE_NUMBER, TYPE_PERCENTAGE]

    def __init__(self):
        super().__init__(summary_type=SummaryType.subjective)

    @classmethod
    def is_valid_subjective_input(cls, content, input_type):
        if input_type not in cls.__subjective_tracking_types:
            return False

        if input_type == TYPE_BOOL:
            return content.__class__ == bool

        if input_type == TYPE_PERCENTAGE:
            correct_type = content.__class__ in [int, float]    
            within_range = 0 <= content <= 100
            return correct_type and within_range

        if input_type == TYPE_NUMBER:
            return content.__class__ in [int, float]    



def get_summary_class_from_type(summary_type: SummaryType):
    
    str_to_class = {
        SummaryType.sleep: Sleep,
        SummaryType.readiness: Readiness,
        SummaryType.activity: Activity,
        SummaryType.bedtime: Bedtime,
        SummaryType.subjective: Subjective
    }

    return str_to_class[summary_type]
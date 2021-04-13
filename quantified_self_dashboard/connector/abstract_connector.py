from typing import Tuple, List, Union
from common.constants import SummaryType

class AbstractConnector:
    """ Abstract class to wrap all the different possible ways of getting data."""
    
    # summary types which this connector is able to load
    supported_summary_types: List[SummaryType] = []

    def __init__(self):
        raise NotImplementedError("Abstract Connector Class")


    def get_summary_data(self, summary_type: SummaryType, date: str) -> Tuple[bool, dict]:
        """
        Retrieves the summary of the given summary type in form of a dictionary.
        Returns also whether the retrieval was successful or not.

        Parameters
        ----------
        summary_type : SummaryType
            Indicating which summary should be retrieved. 

        date : str
            The day the summary is wanted of. 

        Returns
        -------
        Tuple
            bool of whether the retrieval was successful or not
            and result as a dictionary
        """

        raise NotImplementedError("Abstract Connector Class")

    def preload(self, **kwargs):
        """
        Loading all possible supported summaries and preparing data.
        """
        raise NotImplementedError("Abstract Connector Class")


    def get_earliest_and_latest_vailable_summary_date(self) -> Tuple[Union[str, None], Union[str, None]]:
        raise NotImplementedError("Abstract Connector Class")

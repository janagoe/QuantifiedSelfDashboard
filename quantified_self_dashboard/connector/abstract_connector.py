import requests
import json
from typing import Tuple


class AbstractConnector:

    supported_summary_types = []

    def __init__(self):
        raise NotImplementedError("Abstract Connector Class")

    def get_summary(self, summary_type: str, date: str) -> Tuple[bool, dict]:
        """
        Retrieves the summary of the given summary type in form of a dictionary.
        Returns also whether the retrieval was successful or not.

        summary_type : str
            Indicating which summary should be retrieved from the API. 

        date : str
            The day the summary is wanted of. 
        """

        raise NotImplementedError("Abstract Connector Class")


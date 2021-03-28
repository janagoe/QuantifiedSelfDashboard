import os
from typing import List

from summary.summary_container import SummaryContainer



class AbstractStorage:
    """ Abstract class for different methods of saving data. """

    def __init__(self, file_path: List[str]):
        """
        Parameters
        ----------
        file_path : List[str]
            List of strings to the filepath, where the 
            storage file (csv, db) is located.
        """
        self._filename = os.path.join(os.getcwd(), *file_path)


    def save(self, container: SummaryContainer):
        """
        Saving all data from the container in the storage file.

        Parameters
        ----------
        container : SummaryContainer
            The summary container whos summaries will be saved.
        """

        raise NotImplementedError()
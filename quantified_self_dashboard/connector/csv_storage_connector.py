import re
import os
from typing import Tuple, List

import pandas as pd

from common.constants import SummaryType, SUMMARY_DATE
from connector.abstract_connector import AbstractConnector


class CsvStorageConnector(AbstractConnector):
    """ Connector to a csv storage file. """

    # summary types which this connector can load
    supported_summary_types = [SummaryType.sleep, SummaryType.readiness, SummaryType.activity, SummaryType.bedtime, SummaryType.subjective]

    # delimiter of the csv file
    __delimiter = ';'

    def __init__(self, file_path: List[str]):
        """
        Preparing the csv file content for loading.

        Parameters
        ----------
        file_path : List[str]
            The file path to where the csv file with the data can be found.
        """

        self._filename = os.path.join(os.getcwd(), *file_path)
        if not self._filename.endswith('.csv'):
            raise ValueError("Filename for CsvStorageConnector must end with .csv")
        self.__prepare()


    def __prepare(self):
        """ Loading the csv file into a pandas DataFrame. """
        try:
            self.__data = pd.read_csv(self._filename, sep=self.__delimiter)
        except IOError:
            raise ValueError("Could not open file. Please close it first.")


    def get_summary(self, summary_type: SummaryType, date: str) -> Tuple[bool, dict]:
        """
        Retrieves the summary of the given summary type in form of a dictionary
        from the pandas DataFrame.
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
        
        if summary_type not in self.supported_summary_types:
            raise ValueError("Summary Type not supported")

        # preparing regex
        summary_type_column_identifier_re = r'{}_.*'.format(summary_type.name)
        summary_type_suffix_re = r'{}_'.format(summary_type.name)

        # searching for the date row in the DataFrame
        date_entry = self.__data.loc[self.__data[SUMMARY_DATE] == date]
        if len(date_entry) == 0:
            # date is not in the DataFrame
            return False, dict()
        elif len(date_entry) > 1:
            raise AttributeError("Invalid File Content. Too many date entries in one file.")

        # filtering out columns relevant for this summary type
        summary_date_entries = date_entry.loc[:, date_entry.columns.str.match(summary_type_column_identifier_re)]

        # transforming DataFrame into dict
        data = dict()
        data[SUMMARY_DATE] = date
        for column_name in summary_date_entries:
            summary_entry = re.sub(summary_type_suffix_re, '', column_name)
            value = summary_date_entries[column_name].values[0]
            data[summary_entry] = value

        return True, data

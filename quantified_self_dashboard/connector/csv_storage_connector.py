from typing import Tuple, List
from common.constants import *
from connector.abstract_connector import AbstractConnector
import os
import pandas as pd
import re


class CsvStorageConnector(AbstractConnector):

    supported_summary_types = [SLEEP, READINESS, ACTIVITY, BEDTIME, SUBJECTIVE]
    __delimiter = ';'

    def __init__(self, file_path: List[str]):
        self._filename = os.path.join(os.getcwd(), *file_path)
        if not self._filename.endswith('.csv'):
            raise ValueError("Filename for CsvStorageConnector must end with .csv")
        self.__prepare()


    def __prepare(self):
        try:
            self.__data = pd.read_csv(self._filename, sep=self.__delimiter)
        except IOError:
            raise ValueError("Could not open file. Please close it.")


    def get_summary(self, summary_type: str, date: str) -> Tuple[bool, dict]:
        
        if summary_type not in self.supported_summary_types:
            raise AttributeError("Summary Type not supported")

        summary_type_column_identifier_re = r'{}_.*'.format(summary_type)
        summary_type_suffix_re = r'{}_'.format(summary_type)

        date_entry = self.__data.loc[self.__data['summary_date'] == date]
        if len(date_entry) == 0:
            return False, dict()
        elif len(date_entry) > 1:
            raise AttributeError("Too many date entries in one file")

        summary_date_entries = date_entry.loc[:, date_entry.columns.str.match(summary_type_column_identifier_re)]

        data = dict()
        for column_name in summary_date_entries:
            summary_entry = re.sub(summary_type_suffix_re, '', column_name)
            value = summary_date_entries[column_name].values[0]
            data[summary_entry] = value

        return True, data

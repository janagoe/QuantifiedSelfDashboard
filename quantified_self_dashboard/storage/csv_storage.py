from typing import List
import pandas as pd
from storage.abstract_storage import AbstractStorage
from summary.summary_container import SummaryContainer
from common.constants import SUMMARY_DATE


class CsvStorage(AbstractStorage):
    """ Class for saving data in a simple csv file. """

    # delimiter of the csv file
    __delimiter = ';'

    def __init__(self, file_path: List[str]):
        """
        Parameters
        ----------
        file_path : List[str]
            List of strings to the filepath, where the 
            storage csv file is located.
        """

        super().__init__(file_path)
        if not self._filename.endswith('.csv'):
            raise ValueError("Filename for CsvStorage must end with .csv")


    def save(self, container: SummaryContainer, extend=True):
        """
        Saving all data from the container in the csv file.

        Parameters
        ----------
        container : SummaryContainer
            The summary container whos summaries will be saved.
        """

        container_bundle = container.get_dict_of_bundles()
        container_data = pd.DataFrame.from_dict(container_bundle, orient='index')
        container_data.set_index(SUMMARY_DATE, inplace=True)

        try:
            existing_data = pd.read_csv(self._filename, sep=self.__delimiter)
            existing_data.set_index(SUMMARY_DATE, inplace=True)
            
            combined_data = existing_data.combine_first(container_data)
        except:
            combined_data = container_data

        # removing unnamed columns
        # TODO: check this
        combined_data.loc[:,~combined_data.columns.str.match(r'Unnamed.*')]

        # TODO: add try catch
        combined_data.to_csv(self._filename, sep=self.__delimiter)

        
        






        
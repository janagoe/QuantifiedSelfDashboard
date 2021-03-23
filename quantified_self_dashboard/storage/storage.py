
import csv
import os
import pandas as pd
from storage.abstract_storage import AbstractStorage


class CsvStorage(AbstractStorage):

    __delimiter = ';'

    def __init__(self, file_path: List[str]):
        super().__init__(file_path)
        if not self._filename.endswith('.csv'):
            raise ValueError("Filename for CsvStorage must end with .csv")


    def save(self, container: SummaryContainer, extend=True):

        container_bundle = container.get_dict_of_bundles()
        container_data = pd.DataFrame.from_dict(container_bundle, orient='index')
        container_data.set_index('summary_date', inplace=True)

        try:
            existing_data = pd.read_csv(self._filename, sep=self.__delimiter)
            existing_data.set_index('summary_date', inplace=True)
            
            combined_data = existing_data.combine_first(container_data)
        except:
            combined_data = container_data

        # removing unnamed columns
        combined_data.loc[:,~combined_data.columns.str.match(r'Unnamed.*')]

        combined_data.to_csv(self._filename, sep=self.__delimiter)

        
        






        
import requests
import json

from typing import Tuple, List, Union

import pandas as pd

from common.constants import SummaryType, SUMMARY_DATE
from connector.abstract_connector import AbstractConnector

from common.date_helper import *


class OuraApiConnector(AbstractConnector):
    """ Retrieving data from the oura ring API. """

    # summary types which the oura api connector can retrieve
    supported_summary_types = [SummaryType.sleep, SummaryType.readiness, SummaryType.activity, SummaryType.bedtime]

    # template for http requests to the oura api
    __oura_api_request_template = 'https://api.ouraring.com/v1/{}'


    def __init__(self, access_token: str):
        """
        Parameters
        ----------
        access_token : str
            The access token is necessary to get permission to access 
            the personal data from the oura ring API.        
        """
        self.__access_token = access_token


    def __request_summary(self, summary_type: SummaryType, start: str=None, end:str =None) -> requests.Response:
        """
        Calling the Oura API with the summary type and times. 
        Assembling the URL parameters properly with the given parameters.  

        Parameters
        ----------
        summary_type : SummaryType
            Indicating which summary should be retrieved from the API. 

        start : str
            If start is None, it will be set to one week ago.
        
        end : str
            If end is None, it will be set to the current day. 

        Returns
        -------
        requests.Response object
        """

        if summary_type not in OuraApiConnector.supported_summary_types:
            raise ValueError("Summary type not supported by oura API.")

        if not start and not end:
            param_template = "{}?access_token={}"
            params = (summary_type.name, self.__access_token)
        elif start and not end:
            param_template = "{}?start={}&access_token={}"
            params = (summary_type.name, start, self.__access_token)
        elif not start and end:
            param_template = "{}?end={}&access_token={}"
            params = (summary_type.name, end, self.__access_token)
        else: # start and end
            param_template = "{}?start={}&end={}&access_token={}"
            params = (summary_type.name, start, end, self.__access_token)
      
        params_str = param_template.format(*params)
        
        request_str = OuraApiConnector.__oura_api_request_template.format(params_str)
        resp = requests.get(request_str)
      
        return resp


    def get_summary_data(self, summary_type: SummaryType, date: str) -> Tuple[bool, dict]:
        """
        TODO

        Parameters
        ----------
        summary_type : SummaryType
            Indicating which summary should be retrieved from the API. 

        date : str
            The day the summary is wanted of. 

        Returns
        -------
        Tuple
            whether the retrieval was successful or not,
            and the content of the retrieval as a dictionary    
        """

        try:
            summary_date_data = self.__data[summary_type.name][date]
            return True, summary_date_data
        except KeyError:
            # we didnt preload the summary_type-date pair
            # or its not available
            return False, dict()


    @classmethod
    def response_to_dict(cls, response_obj: requests.Response) -> dict:
        """ Transforming the response object into a dictionary """
        answer_dict = response_obj.json()
        answer_str = json.dumps(answer_dict)
        answer_json = json.loads(answer_str)
        return answer_json


    @classmethod
    def make_uniform(cls, resp_content: dict) -> dict:
        """ 
        Changing the dictionary for the bedtime summary type
        to make the response match the response format of the other summary types.
        Nothing changes for other summary types.
        """
        summary_type_str = list(resp_content.keys())[0]

        if summary_type_str == "ideal_bedtimes":

            # changing 'ideal_bedtime' key to 'bedtime'
            summary_type_str = SummaryType.bedtime.name
            resp_content[summary_type_str] = resp_content.pop("ideal_bedtimes")

            for i in range(len(resp_content[summary_type_str])):
                current = resp_content[summary_type_str][i]

                # changing 'date' key to 'summary_date'
                current[SUMMARY_DATE] = current.pop('date')

                # moving the nested dictionary to two additional keys
                bedtime_window_dict = current.pop('bedtime_window')
                current['bedtime_window_start'] = bedtime_window_dict['start']
                current['bedtime_window_end'] = bedtime_window_dict['end']
                
        return resp_content
    

    def preload(self, **kwargs):
        everything = False
        if 'everything' in kwargs.keys():
            everything = kwargs['everything']

        if everything:
            self.__preload_everything()
        else: 
            earliest = kwargs['earliest_available_date']
            latest = kwargs['latest_available_date']
            missing_dates = kwargs['missing_dates']
            self.__preload_considering_missing_data(earliest, latest, missing_dates)

    


    def __load_data(self, start: str=None, end:str =None):
        """
        Requesting and formating data from start to end for all supported summary types.
        """

        merged_data = dict()
        summary_count = 0

        for summary_type in self.supported_summary_types:

            resp = self.__request_summary(summary_type, start, end)
            status = resp.status_code

            if not (200 <= status < 300):
                continue

            content: dict = OuraApiConnector.response_to_dict(resp)
            uniform_content: dict = OuraApiConnector.make_uniform(content)
            summary_count += len(list(uniform_content.values())[0])

            merged_data.update(uniform_content)

        return merged_data, summary_count


    def __load_data(self, date: str):
        return self.__load_data(date, date)


    def __preload_everything(self):
        current_end_date = datetime_to_simple_iso(datetime.today())
        nothing_loaded_before = False

        list_of_dict_bundles = []

        while True:
            current_start_date = get_one_week_before(current_end_date)
            current_data, summary_count = self.__load_data(current_start_date, current_end_date)

            list_of_dict_bundles.append(current_data)

            if summary_count == 0:
                if nothing_loaded_before:
                    break
                else:
                    nothing_loaded_before = True
            current_end_date = current_start_date

        self.__merging_and_saving_list_of_dict_bundles(list_of_dict_bundles)
        
                

    def __preload_considering_missing_data(self, missing_data_before_date: str, missing_data_after_date: str, missing_after_in_between: List[str]):
        """
        TODO
        Everything before the missing_data_before_date (exclusive)
        Everything after the missing_data_after_date (exclusive)
        Every date given in missing_after_in_between
        """

        list_of_dict_bundles = []

        # loading everything before
        current_end_date = get_day_before(missing_data_before_date)
        while True:
            current_start_date = get_one_week_before(current_end_date)
            current_data, summary_count = self.__load_data(current_start_date, current_end_date)

            list_of_dict_bundles.append(current_data)

            if summary_count == 0:
                if nothing_loaded_before:
                    break
                else:
                    nothing_loaded_before = True
            current_end_date = current_start_date

        # loading everything after
        current_end_date = get_day_after(missing_data_after_date)
        while True:
            current_start_date = get_one_week_after(current_end_date)
            current_data, summary_count = self.__load_data(current_start_date, current_end_date)

            list_of_dict_bundles.append(current_data)

            if summary_count == 0:
                if nothing_loaded_before:
                    break
                else:
                    nothing_loaded_before = True
            current_end_date = current_start_date

        # loading the missing dates in between
        for date in missing_after_in_between:
            current_data, summary_count = self.__load_data(date)
            if summary_count == 0:
                list_of_dict_bundles.append(current_data)

        self.__merging_and_saving_list_of_dict_bundles(list_of_dict_bundles)



    def __merging_and_saving_list_of_dict_bundles(self, list_of_dict_bundles):
        """ TODO """
        merged_dicts = dict()
        if len(list_of_dict_bundles) > 0:

            for one_dict_bundle in list_of_dict_bundles:
                for summary_type_str in one_dict_bundle.keys():
                    
                    if summary_type_str not in merged_dicts.keys():
                        merged_dicts[summary_type_str] = dict()

                    for one_summary_data in one_dict_bundle[summary_type_str]:
                        merged_dicts[summary_type_str][one_summary_data[SUMMARY_DATE]] = one_summary_data
                
        self.__data = merged_dicts


    def get_earliest_and_latest_vailable_summary_date(self) -> Tuple[Union[str, None], Union[str, None]]:
        earliest_list, latest_list = [], []
        for summary_type_str in self.__data.keys():
            keys = self.__data.keys()
            earliest_list.append(min(keys))
            latest_list.append(min(keys))

        earliest = min(earliest_keys)
        latest = max(latest_keys)

        return earliest, latest
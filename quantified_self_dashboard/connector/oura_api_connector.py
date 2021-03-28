import requests
import json

from typing import Tuple

from common.constants import SummaryType, SUMMARY_DATE
from connector.abstract_connector import AbstractConnector



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


    def get_summary(self, summary_type: SummaryType, date: str) -> Tuple[bool, dict]:
        """
        Requests the summary and checking for HTML errors.
        In case of no errors, returning the response as a dictionary.

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

        resp = self.__request_summary(summary_type, date, date)
        status = resp.status_code

        if not (200 <= status < 300):
            return False, dict()

        content: dict = OuraApiConnector.response_to_dict(resp)
        uniform_content: dict = OuraApiConnector.make_uniform(content)

        # if multiple dates would have been requested
        # there would be multiple elemtends in this list
        list_of_contents: List[dict] = uniform_content[summary_type.name]

        if len(list_of_contents) == 1: 
            return True, list_of_contents[0]

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
        
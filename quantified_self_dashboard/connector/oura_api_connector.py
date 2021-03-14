import requests
import json
from typing import Tuple

from common.constants import *
from connector.abstract_connector import AbstractConnector



class OuraApiConnector(AbstractConnector):

    __oura_api_request_template = 'https://api.ouraring.com/v1/{}'
    __oura_summary_types = [SLEEP, READINESS, ACTIVITY, BEDTIME]

    def __init__(self, access_token):
        self.__access_token = access_token

    def __request_summary(self, summary_type: str, start: str=None, end:str =None) -> requests.Response:
        """
        Calling the Oura API with the summary type and times. 
        Assembling the URL parameters properly with the given parameters.  

        summary_type : str
            Indicating which summary should be retrieved from the API. 

        start : str
            If start is None, it will be set to one week ago.
        
        end : str
            If end is None, it will be set to the current day. 
        """

        if summary_type not in OuraApiConnector.__oura_summary_types:
            raise ValueError("Summary type not supported by oura API.")

        if not start and not end:
            param_template = "{}?access_token={}"
            params = (summary_type, self.__access_token)
        elif start and not end:
            param_template = "{}?start={}&access_token={}"
            params = (summary_type, start, self.__access_token)
        elif not start and end:
            param_template = "{}?end={}&access_token={}"
            params = (summary_type, end, self.__access_token)
        else: # start and end
            param_template = "{}?start={}&end={}&access_token={}"
            params = (summary_type, start, end, self.__access_token)
      
        params_str = param_template.format(*params)
        
        request_str = OuraApiConnector.__oura_api_request_template.format(params_str)
        resp = requests.get(request_str)
      
        return resp

    def get_summary(self, summary_type: str, date: str) -> Tuple[bool, dict]:
        """
        Requests the summary and checking for HTML errors.
        In case of no errors, returning the response as a dictionary.
        Also returning whether the retrieval of the summary was succesful or not.

        summary_type : str
            Indicating which summary should be retrieved from the API. 

        date : str
            The day the summary is wanted of. 
        """

        resp = self.__request_summary(summary_type, date, date)
        status = resp.status_code

        if not (200 <= status < 300):
            return False, dict()

        content = OuraApiConnector.response_to_dict(resp)
        uniform_content = OuraApiConnector.make_uniform(content)

        summary_type = list(uniform_content.keys())[0]
        list_of_contents = uniform_content[summary_type]
        if len(list_of_contents) > 0: 
            return True, list_of_contents[0]

        return False, dict()


    @classmethod
    def response_to_dict(cls, response_obj: requests.Response) -> dict:
        answer_dict = response_obj.json()
        answer_str = json.dumps(answer_dict)
        answer_json = json.loads(answer_str)
        return answer_json


    @classmethod
    def make_uniform(cls, resp_content: dict) -> dict:
        summary_type = list(resp_content.keys())[0]

        if summary_type == "ideal_bedtimes":
            summary_type = BEDTIME
            resp_content[summary_type] = resp_content.pop("ideal_bedtimes")

            for i in range(len(resp_content[summary_type])):
                current = resp_content[summary_type][i]
                current['summary_date'] = current.pop('date')
                
        return resp_content
        
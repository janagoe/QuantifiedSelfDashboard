import requests
import json
from constants import *



class OuraApiConnector:

    oura_api_request_template = 'https://api.ouraring.com/v1/{}'
    oura_summary_types = [SLEEP, READINESS, ACTIVITY, BEDTIME, USERINFO]

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

        if summary_type not in OuraApiConnector.oura_summary_types:
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
        
        request_str = OuraApiConnector.oura_api_request_template.format(params_str)
        resp = requests.get(request_str)
      
        return resp

    def get_summary(self, summary_type: str, start=None, end=None) -> dict:
        """
        Requests the summary and checking for HTML errors.
        In case of no errors, returning the response as a dictionary.

        summary_type : str
            Indicating which summary should be retrieved from the API. 

        start : str
            If start is None, it will be set to one week ago.
        
        end : str
            If end is None, it will be set to the current day. 
        """

        resp = self.__request_summary(summary_type, start, end)
        content = OuraApiConnector.response_to_dict(resp)

        status = resp.status_code
        if 400 <= status < 500:
            error_title = content['title']
            raise RuntimeError("There is a problem with the sent request: {}".format(error_title))
        elif 500 <= status < 600:
            raise RuntimeError("Oura Server Error.")
        elif 200 <= status < 300:
            return content
        else: 
            raise RuntimeError("Undefined Response Status.")

    @classmethod
    def response_to_dict(cls, response_obj: requests.Response) -> dict:
        answer_dict = response_obj.json()
        answer_str = json.dumps(answer_dict)
        answer_json = json.loads(answer_str)
        return answer_json
        
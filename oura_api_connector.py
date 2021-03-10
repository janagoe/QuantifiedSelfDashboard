import requests
import json

class OuraApiConnector:

    oura_api_request_template = 'https://api.ouraring.com/v1/{}'
    oura_summary_types = ['bedtime', 'sleep', 'readiness', 'activity', 'userinfo']

    def __init__(self, access_token):
        self.__access_token = access_token

    def request_summary(self, summary_type, start=None, end=None):
        # for now assuming that start and end dates are given as strings

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

    def get_summary(self, summary_type, start=None, end=None):
        
        resp = self.request_summary(summary_type, start, end)
        content = OuraApiConnector.response_to_json(resp)

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
    def response_to_json(cls, response_obj):
        answer_dict = response_obj.json()
        answer_str = json.dumps(answer_dict)
        answer_json = json.loads(answer_str)
        return answer_json
        
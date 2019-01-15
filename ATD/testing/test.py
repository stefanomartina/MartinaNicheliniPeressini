import unittest, requests, json


class Test(unittest.TestCase):

    #URL_BASE_ENDPOINT = "https://data4halp.herokuapp.com"
    URL_BASE_ENDPOINT = "https://data4halp.herokuapp.com"

    def __post__(self, specific_url_endpoint, parameters):
        URL = self.URL_BASE_ENDPOINT + specific_url_endpoint
        parameters = json.load(parameters)
        post_request = requests.post(URL, json=parameters)
        return post_request.status_code

    def __get__(self, specific_url_endpoint, parameters):
        URL = self.URL_BASE_ENDPOINT + specific_url_endpoint
        parameters = json.load(parameters)
        get_request = requests.get(URL, json=parameters)
        return get_request.status_code

    def registration_test(self):
        URL = "/v1/auth/register_user"
        parameters = {
            "mail": "test@test.mail",
            "password": "password",
            "SSN": "prova",
            "name": "test",
            "surname": "test_surname",
            "birthday": "1999-05-06",
            "smartwatch": "AppleWatch"
        }

        status_code = self.__post__(parameters, URL)
        self.assertEqual(status_code, '200')

if __name__ == '__main__':
    unittest.main()

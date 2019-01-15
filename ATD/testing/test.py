import unittest, requests, json


class Test(unittest.TestCase):

    #URL_BASE_ENDPOINT = "https://data4halp.herokuapp.com"
    URL_BASE_ENDPOINT = "https://data4halp.herokuapp.com"

    def __post__(self, specific_url_endpoint, parameters):
        URL = self.URL_BASE_ENDPOINT + specific_url_endpoint
        #parameters = json.load(parameters)
        post_request = requests.post(URL, json=parameters)
        return post_request

    def __get__(self, specific_url_endpoint, parameters):
        URL = self.URL_BASE_ENDPOINT + specific_url_endpoint
        parameters = json.load(parameters)
        get_request = requests.get(URL, json=parameters)
        return get_request.status_code

    def test_registration_user(self):
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

        response = self.__post__(URL, parameters)
        status_code = response.status_code

        self.assertEqual(str(status_code), '200')
        print(response.content)

    def test_registration_company(self):
        URL = "/v1/auth/register_company"


if __name__ == '__main__':
    unittest.main()

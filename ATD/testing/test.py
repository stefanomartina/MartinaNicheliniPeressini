import unittest, requests, json


class Test(unittest.TestCase):

    #URL_BASE_ENDPOINT = "https://data4halp.herokuapp.com"
    URL_BASE_ENDPOINT = "http://data4help.cloud:12345"

    def __post__(self, specific_url_endpoint, parameters):
        URL = self.URL_BASE_ENDPOINT + specific_url_endpoint
        post_request = requests.post(URL, json=parameters)
        return post_request

    def __get__(self, specific_url_endpoint, parameters):
        URL = self.URL_BASE_ENDPOINT + specific_url_endpoint
        get_request = requests.get(URL, json=parameters)
        return get_request.status_code

    def test_registration_user(self):
        URL = "/v1/auth/register_user"
        parameters = {
            'email': 'example@gmail.com',
            'password': '12344',
            'SSN': '0123456789012345',
            'name': 'test',
            'surname': 'test_surname',
            'birthday': '1999-05-06',
            'smartwatch': 'AppleWatch'
        }
        parameters={
            "email": "georgemesaclooney@gmail.com",
            "password": "asdfasdf",
            "SSN": "TESTTESTTESTTEST",
            "name": "George",
            "surname": "Clooney",
            "birthday": "1999-05-06",
            "smartwatch": "TEST Smartwatch"
        }

        response = self.__post__(URL, parameters)
        status_code = response.status_code

        self.assertEqual(str(status_code), '200')
        print(response.content)

    def test_registration_company(self):
        URL = "/v1/auth/register_company"
        parameters = {
            'email': 'example@gmail.com',
            'password': '125345345',
            'company_name': 'redbull',
        }
        response = self.__post__(URL, parameters)
        status_code = response.status_code

        self.assertEqual(str(status_code), '200')
        print(response.content)



if __name__ == '__main__':
    unittest.main()

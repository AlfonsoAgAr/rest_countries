import sys; sys.path.append('../')
import unittest

from src import Client

path_responses = 'request_response/'

class RequestTest(unittest.TestCase):

    def test_request_successful_connect(self):
        # Connnection successful must return code 200
        self.assertEqual(Client().get_by_language('english').status, [200])
        # Connection successful with a bad path must return code 404
        self.assertEqual(Client().get_by_language('englizh').status, [404])

    def test_correct_base_path(self):
        case = 'restcountries.com'
        # If base url is not defined, the base path is restcountries.com
        self.assertEqual(Client().base_url, case)
        
    def test_correct_asign_path(self):
        cases = ['google.com', 'facebook.com', 'youtube.com', 'instagram.com', 'twitter.com']

        for case in cases:
            # Case must be equal to the base_url
            self.assertEqual(Client(base_url=case).base_url, case)
            # In this case the base path is constant. And random.com != google.com, random.com != facebook.com, etc.
            self.assertNotEqual(Client(base_url='random.com').base_url, case)

    def test_request_get(self):
        # Test a method not implemented in class
        cases = ['mexico', 'colombia', 'peru']
        
        for country in cases:
            with open(path_responses + f'{country}.json', 'r') as file:
                # Return data from the country and compare it with the data from the file
                # +2500 characters are compared
                self.assertEqual(Client().get(path=f'/v3.1/name/{country}').text, file.read())

    
if __name__ == '__main__':
    unittest.main()

# For run  
# python3 -m unittest request_test -v
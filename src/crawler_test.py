import unittest
import requests
from unittest.mock import MagicMock, patch
from crawler import Crawler
import json

class CrawlerTest(unittest.TestCase):
    @patch('crawler.requests.get')
    def test_fetch_success(self, mock_get):
        # Mock response data
        response_data = {
            "data": {
                "quotes": [
                    {
                        "quote": {
                            "Open": 100,
                            "High": 120,
                            "Low": 90,
                            "Close": 110,
                            "Volume": 1000,
                            "Market_Cap": 5000,
                            "Time": 1622182200000
                        }
                    },
                    {
                        "quote": {
                            "Open": 110,
                            "High": 130,
                            "Low": 100,
                            "Close": 120,
                            "Volume": 1500,
                            "Market_Cap": 6000,
                            "Time": 1622268600000
                        }
                    }
                ]
            }
        }
        
        # Configure mock response
        mock_response = MagicMock()
        mock_response.text = json.dumps(response_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Create an instance of the Crawler class
        crawler = Crawler()
        
        # Define input parameters
        crypto_id = 1
        time_start = 1622182200000
        time_end = 1622268600000
        symbol = 'BTC'
        
        # Call the fetch method
        result = crawler.fetch(crypto_id, time_start, time_end, symbol)
        
        # Verify the expected DataFrame structure
        expected_columns = ['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market_Cap', 'Time']
        self.assertEqual(result.columns.tolist(), expected_columns)
        self.assertEqual(result['Symbol'].tolist(), ['BTC', 'BTC'])
        self.assertEqual(result['Open'].tolist(), [100, 110])
        self.assertEqual(result['High'].tolist(), [120, 130])
        self.assertEqual(result['Low'].tolist(), [90, 100])
        self.assertEqual(result['Close'].tolist(), [110, 120])
        self.assertEqual(result['Volume'].tolist(), [1000, 1500])
        self.assertEqual(result['Market_Cap'].tolist(), [5000, 6000])
        self.assertEqual(result['Time'].tolist(), [1622182200000, 1622268600000])
        
        # Verify that the requests.get method was called with the correct arguments
        mock_get.assert_called_once_with(
            "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical",
            {
                "id": crypto_id,
                "convertId": 2781,
                "timeStart": time_start,
                "timeEnd": time_end
            }
        )
        

    @patch.object(requests, 'get')
    def test_fetch_http_error(self, mock_get):
        # Configure mock response with HTTP error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        # Create an instance of the Crawler class
        crawler = Crawler()

        # Call the fetch method and verify that it raises a RuntimeError
        with self.assertRaises(RuntimeError):
            crawler.fetch(1, 1622182200000, 1622268600000, 'BTC')
        
    @patch('crawler.requests.get')
    def test_fetch_json_error(self, mock_get):
        # Configure mock response with invalid JSON
        mock_response = MagicMock()
        mock_response.text = "Invalid JSON response"
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Create an instance of the Crawler class
        crawler = Crawler()
        
        # Call the fetch method and verify that it raises a RuntimeError
        with self.assertRaises(RuntimeError):
            crawler.fetch(1, 1622182200000, 1622268600000, 'BTC')

if __name__ == '__main__':
    unittest.main()
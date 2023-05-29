import requests
import json
import pandas as pd

class Crawler:
  def fetch(self, crypto_id, time_start, time_end, symbol):  
    API_ENDPOINT = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical"
    
    try:
        response = requests.get(API_ENDPOINT, {
           "id": crypto_id,
           "convertId": 2781, #USD Conversion ID
           "timeStart": time_start,
           "timeEnd": time_end
        })

        response.raise_for_status() 

        data = json.loads(response.text)
        quotes = data["data"]["quotes"]

        result = []

        for quote in quotes:
            values = quote["quote"].values()
            result.append(list(values))

        df = pd.DataFrame(result, columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Market_Cap', 'Time'])
        df.insert(0, 'Symbol', symbol)

        return df

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error occurred during the HTTP request: {e}")

    except (KeyError, json.JSONDecodeError):
        raise RuntimeError("Error occurred while parsing the JSON response.")

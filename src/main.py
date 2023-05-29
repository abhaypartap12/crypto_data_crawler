import requests
import json
import pandas as pd
import time

from crawler import Crawler
from uploder import Uploader
from analyzer import Analyser

from util import merge_dataframes


def main(look_back_days):

    file_path = 'data.csv'

    crypto_data = {
        1: 'BTC',
        1027: 'ETH'
    }

    seconds_per_day = 60 * 60 * 24
    time_start = int(time.time()) - (look_back_days * seconds_per_day)
    time_end = int(time.time())

    dataframes = []
    crawler = Crawler()

    for crypto_id, symbol in crypto_data.items():
        historical_data = crawler.fetch(crypto_id, time_start, time_end, symbol)
        dataframes.append(historical_data)

    merged_dataframe = merge_dataframes(dataframes)
    merged_dataframe.to_csv(file_path, index=False)
    print("CSV file created successfully.")

    Uploader().upload_to_gcs(file_path)
    Analyser().analyse(file_path)
    

if __name__ == '__main__':
    try:
        main(look_back_days=60)

    except Exception as e:
       print(f"An error occurred: {e}")

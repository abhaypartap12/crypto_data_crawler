
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Analyser:

    def analyse_data(self, data, symbol):
        print(f"----- Report for {symbol}----------")
        print('Mean:',data['Close'].mean())
        print('Min:',data['Close'].min())
        print('Max:',data['Close'].max())
        print('Standard Dev:',data['Close'].std())
        
        # Using describe function
        print(data.describe())


    def plot_graph(self, data, trend, param):
        #Graph size
        plt.figure(figsize=(15, 8))

        # Plotting the line graph
        plt.plot(data['Time'], data[param], linewidth=2)

        # Adding labels and title
        plt.title(trend)
        plt.xlabel('Time')
        plt.ylabel(param)

        # Displaying the graph
        plt.show()

    def analyse(self, file_path):
        df = pd.read_csv(file_path) #import data from csv file
        # Convert the 'date' column to datetime type
        df['Time'] = pd.to_datetime(df['Time'])


        # Get the current date
        current_date = datetime.now().date()

        # Calculate the date 30 days ago
        start_date = current_date - timedelta(days=30)

        df['Date'] = df['Time'].apply(lambda x: x.date())

        df = df[df['Date']> start_date]
        df.info()

        # Extract the data for the month of May
        may_data = df[df['Time'].dt.month == 5]

        # Extract the data for BTC
        btc_data = may_data[may_data['Symbol'] == 'BTC']

        # Extract the data for ETH
        eth_data = may_data[may_data['Symbol'] == 'ETH']

        self.analyse_data(btc_data, "BTC")
        self.analyse_data(eth_data, "ETH")


        #print(btc_data.corrwith(eth_data, method='spearman'))

        #print('Using Box Plot for outlier detection')
        #print('The dots in the box plots correspond to extreme outlier values.') 

        sns.boxplot(data=btc_data,x=btc_data["Close"])
        plt.title("Boxplot of Closing Price of BTC")

        sns.boxplot(data=eth_data,x=eth_data["Close"])
        plt.title("Boxplot of Closing Price of ETH")

        #print('Using Line Graph for finding any trend in closing price of ')


        self.plot_graph(btc_data, "Price", "Close")  
        self.plot_graph(eth_data, "Price", "Close")  
        self.plot_graph(btc_data, "Price", "Volume")  
        self.plot_graph(btc_data, "Price", "Volume")  

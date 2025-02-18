import json
import requests
import matplotlib.pyplot as plt
import time

def main():
    with open('api_key.json', 'r') as file:
        api_json_data = json.load(file)
        
    API_KEY = api_json_data.get("key")
    
    # Create interactive plot and set size
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis
    
    while True:
        
        if not API_KEY:
            raise ValueError("API key not found. Please set ALPHA_VANTAGE_API_KEY in your .env file.")
        
        requestFailed:bool = True
        data = 0
        while requestFailed:
            requestFailed = False
            
            print("Enter a stock market symbol: ", end="")
            userInput = input()
        
            # Endpoint for daily time series data
            endpoint = "https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": userInput,
                "apikey": API_KEY,
                "outputsize": "compact"
            }
            
            try:
                print(f"Sending get request for '{userInput}'.....\n{params}")
                response = requests.get(endpoint, params=params)
                # Check status code
                response.raise_for_status() # raises HTTPError if status != 200
                
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while making request: {e}")
                requestFailed = True
        
            if not requestFailed:
                # Parse JSON
                print("Getting Data...")
                data = response.json()
                
                # Check if valid data was returned
                if "Time Series (Daily)" not in data:
                    print("Unexpected data format received. Check API parameters and usage limits.")
                    print("==================================")
                    print(data)
                    requestFailed = True
            
        try:
            time_series = data["Time Series (Daily)"]
        
        except KeyError:
            print(data)
            return
            
        # We’ll extract the date and closing price
        dates = []
        closing_prices = []
        
        # Sort the dates so oldest is first
        sorted_dates = sorted(time_series.keys())
        
        for date in sorted_dates:
            closing_price = float(time_series[date]["4. close"])
            dates.append(date)
            closing_prices.append(closing_price)
            
        # Plotting
        
        # plt.figure(figsize=(10, 6))
        # plt.plot(dates, closing_prices, marker='o', linewidth=1)
        # plt.title("IBM Stock Price (Daily Close)")
        # plt.xlabel("Date")
        # plt.ylabel("Closing Price (USD)")
        # plt.xticks(rotation=45) # Rotate dates to avoid overlap
        # plt.tight_layout()
        # plt.show()
        
        print("updating plots...")
        # print(response.json()["Time Series (Daily)"])
        ax.plot(dates, closing_prices, marker='o', linewidth=1, label=f'{userInput} Stock Price: {response}')
        ax.set_title("IBM Stock Price (Daily Close)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Closing Price (USD)")
        ax.tick_params(axis='x', rotation=45) # Rotate dates to avoid overlap
        ax.legend()
        plt.tight_layout()
        plt.draw()
        
        print("\nPlot updated. Enter another symbol or Ctrl+C to exit.")
        time.sleep(2)  # Sleep to prevent too rapid updates

if __name__ == "__main__": main()
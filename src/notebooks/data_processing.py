# data_processing.py

import pandas as pd
from config import file_path, start_date, end_date

class MACDDataProcessor:
    def __init__(self, csv_file_path: str):
        self.data = pd.read_csv(csv_file_path, parse_dates=['date'])
        self.data.set_index('date', inplace=True)

    def filter_data(self, start_date: str, end_date: str):
        self.filtered_data = self.data.loc[start_date:end_date]

    def calculate_ema(self, period: int):
        return self.filtered_data['close'].ewm(span=period, adjust=False).mean()

    def calculate_macd(self):
        ema_short = self.calculate_ema(12)
        ema_long = self.calculate_ema(26)
        macd = ema_short - ema_long
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        return ema_short, ema_long, macd, signal, histogram

    def get_filtered_data(self):
        return self.filtered_data.to_dict()

    def get_macd_components(self):
        ema_short, ema_long, macd, signal, histogram = self.calculate_macd()
        return {
            'ema_short': ema_short.to_dict(),
            'ema_long': ema_long.to_dict(),
            'macd': macd.to_dict(),
            'signal': signal.to_dict(),
            'histogram': histogram.to_dict()
        }

    def inspect_data(self):
        print("Filtered Data Info:")
        print(self.filtered_data.info())
        ema_short, ema_long, macd, signal, histogram = self.calculate_macd()
        print("EMA Short Length:", len(ema_short))
        print("EMA Long Length:", len(ema_long))
        print("MACD Length:", len(macd))
        print("Signal Length:", len(signal))
        print("Histogram Length:", len(histogram))
        print("Filtered Data Head:\n", self.filtered_data.head())
        print("EMA Short Head:\n", ema_short.head())
        print("EMA Long Head:\n", ema_long.head())
        print("MACD Head:\n", macd.head())
        print("Signal Head:\n", signal.head())
        print("Histogram Head:\n", histogram.head())

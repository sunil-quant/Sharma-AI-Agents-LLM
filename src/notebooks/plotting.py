# plotting.py

import pandas as pd
import numpy as np
import mplfinance as mpf
from data_processing import MACDDataProcessor

class MACDPlotter:
    def __init__(self, csv_file_path: str):
        self.processor = MACDDataProcessor(csv_file_path)

    def plot_macd(self, start_date: str, end_date: str, save_path: str, plot_type: str = "candle", plot_style: str = "default", show_nontrading: bool = False):
        self.processor.filter_data(start_date, end_date)
        ema_short, ema_long, macd, signal, histogram = self.processor.calculate_macd()

        crossover_points = ((macd.shift(1) > signal.shift(1)) & (macd <= signal)) | ((macd.shift(1) < signal.shift(1)) & (macd >= signal))

        lengths = [len(ema_short), len(ema_long), len(macd), len(signal), len(histogram)]
        print("Lengths of MACD components:", lengths)
        if len(set(lengths)) != 1:
            print(f"Length inconsistency detected: {lengths}")
            return f"Error: Length inconsistency detected in MACD components. Lengths: {lengths}"

        ema_short_plot = mpf.make_addplot(ema_short, color='red', width=2.0, secondary_y=False, label='EMA Short')
        ema_long_plot = mpf.make_addplot(ema_long, color='green', width=2.0, secondary_y=False, label='EMA Long')

        crossover_series = pd.Series(np.nan, index=macd.index)
        crossover_series[crossover_points] = macd[crossover_points].values

        crossover_plot = mpf.make_addplot(crossover_series, type='scatter', markersize=50, marker='o', color='purple', panel=2, label='Crossovers')

        histogram_positive = histogram.where(histogram >= 0)
        histogram_negative = histogram.where(histogram < 0)

        histogram_positive_plot = mpf.make_addplot(histogram_positive, panel=2, type='bar', color='green', secondary_y=False, width=0.8)
        histogram_negative_plot = mpf.make_addplot(histogram_negative, panel=2, type='bar', color='red', secondary_y=False, width=0.8)
        macd_plot = mpf.make_addplot(macd, panel=2, color='blue', width=2.0, secondary_y=False, label='MACD', ylabel='MACD')
        signal_plot = mpf.make_addplot(signal, panel=2, color='magenta', width=2.0, secondary_y=False, label='Signal')

        apds = [ema_short_plot, ema_long_plot, histogram_positive_plot, histogram_negative_plot, macd_plot, signal_plot, crossover_plot]

        plot_params = {
            "type": plot_type,
            "style": plot_style,
            "addplot": apds,
            "volume": True,
            "title": "MACD with EMA and Histogram",
            "show_nontrading": show_nontrading,
            "savefig": save_path,
            "tight_layout": True,
            "figscale": 1.5,
            "figsize": (10, 6),
            "datetime_format": '%b %Y',
            "panel_ratios": (5, 2, 6)
        }

        fig, axlist = mpf.plot(self.processor.filtered_data, **plot_params, returnfig=True)

        fig.subplots_adjust(top=0.9, right=0.75)
        fig.suptitle('MACD with EMA and Histogram', y=0.95, fontsize=12)

        legend_lines_main = [
            axlist[0].plot([], [], color='red', linewidth=2, label='EMA Short')[0],
            axlist[0].plot([], [], color='green', linewidth=2, label='EMA Long')[0]
        ]
        legend_lines_macd = [
            axlist[2].plot([], [], color='blue', linewidth=2, label='MACD')[0],
            axlist[2].plot([], [], color='magenta', linewidth=2, label='Signal')[0]
        ]
        legend_lines_crossover = [
            axlist[2].plot([], [], color='purple', marker='o', markersize=10, linestyle='None', label='Crossovers')[0]
        ]

        axlist[2].bar([], [], color='green', label='Histogram Positive')
        axlist[2].bar([], [], color='red', label='Histogram Negative')

        axlist[0].legend(handles=legend_lines_main, loc='upper left', bbox_to_anchor=(1.05, 1))
        axlist[2].legend(handles=legend_lines_macd, loc='upper left', bbox_to_anchor=(1.05, 0.5))
        axlist[2].legend(handles=legend_lines_crossover, loc='upper left', bbox_to_anchor=(1.05, 0))

        plt.close(fig)

        return f"MACD chart saved to {save_path}"

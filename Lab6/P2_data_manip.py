"""
Chatchana Chaenban
683040487-6
P2
"""

import json
import numpy as np
import pandas as pd
import pyqtgraph as pg

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS - do not change
# ══════════════════════════════════════════════════════════════════════════

REQUIRED_COLS = {"date", "city", "temp_c", "humidity", "rainfall_mm", "condition"}
CONDITIONS    = ["Sunny", "Cloudy", "Rainy", "Stormy"]
CITIES        = ["Bangkok", "Chiang Mai", "Phuket"]


# ══════════════════════════════════════════════════════════════════════════
#  YOUR WORK — complete the 6 functions below
# ══════════════════════════════════════════════════════════════════════════

def read_csv(path: str) -> pd.DataFrame:
    """
    To do 1 — Read a CSV file and return a clean DataFrame.
    """
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("The CSV file is empty.")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    return df


def read_json(path: str) -> pd.DataFrame:
    """
    To do 2 — Read a JSON file and return a DataFrame.
    """
    df = pd.read_json(path)

    if df.empty:
        raise ValueError("The JSON file is empty.")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"JSON is missing required columns: {missing}")

    return df


def write_csv(df: pd.DataFrame, path: str) -> None:
    """
    To do 3 — Save a DataFrame to a CSV file.
    """
    if df.empty:
        raise ValueError("Cannot save an empty DataFrame to CSV.")

    try:
        df.to_csv(path, index=False)
    except Exception as e:
        raise IOError(f"Error writing CSV file: {e}")


def write_json(df: pd.DataFrame, path: str) -> None:
    """
    To do 4 — Save a DataFrame to a JSON file.
    """
    if df.empty:
        raise ValueError("Cannot save an empty DataFrame to JSON.")

    try:
        df.to_json(path, orient="records", indent=2)
    except Exception as e:
        raise IOError(f"Error writing JSON file: {e}")


def build_stats(df: pd.DataFrame) -> QTableWidget:
    """
    To do 5 — Return a QTableWidget shown in the Statistics panel.
    """
    if df.empty:
        raise ValueError("DataFrame is empty.")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame is missing required columns: {missing}")

    cities = sorted(df["city"].unique())
    row_labels = ["count", "avg_temp", "max_temp", "min_temp", "total_rain", "avg_humidity"]

    table = QTableWidget(len(row_labels), len(cities))
    table.setHorizontalHeaderLabels(cities)
    table.setVerticalHeaderLabels(row_labels)
    table.horizontalHeader().setStretchLastSection(True)

    for col_idx, city in enumerate(cities):
        city_df = df[df["city"] == city]

        values = [
            str(len(city_df)),
            f"{city_df['temp_c'].mean():.1f}",
            f"{city_df['temp_c'].max():.1f}",
            f"{city_df['temp_c'].min():.1f}",
            f"{city_df['rainfall_mm'].sum():.1f}",
            f"{city_df['humidity'].mean():.1f}",
        ]

        for row_idx, val in enumerate(values):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_idx, col_idx, item)

    table.resizeColumnsToContents()
    return table


def show_chart(df: pd.DataFrame, chart_type: str) -> pg.PlotWidget:
    """
    To do 6 — Draw a Rainfall Histogram chart using pyqtgraph and return a PlotWidget.
    """
    if df.empty:
        raise ValueError("DataFrame has no data.")

    if "rainfall_mm" not in df.columns:
        raise ValueError("Column 'rainfall_mm' not found in DataFrame.")

    rainfall = df["rainfall_mm"].dropna().values
    counts, bin_edges = np.histogram(rainfall, bins=10)

    plot_widget = pg.PlotWidget()
    plot_widget.setBackground("w")
    plot_widget.setTitle("Rainfall Histogram", color="k", size="12pt")
    plot_widget.setLabel("left", "Frequency")
    plot_widget.setLabel("bottom", "Rainfall (mm)")

    bar_item = pg.BarGraphItem(
        x=bin_edges[:-1],
        height=counts,
        width=(bin_edges[1] - bin_edges[0]) * 0.9,
        brush=pg.mkBrush(70, 130, 200, 200),
        pen=pg.mkPen("w"),
    )
    plot_widget.addItem(bar_item)

    return plot_widget

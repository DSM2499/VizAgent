import pandas as pd
import numpy as np
import ydata_profiling
import sweetviz
import os
from io import StringIO
from datetime import datetime

def generate_descriptive_stats(df: pd.DataFrame) -> dict:
    desc_stats = {
        "shape": df.shape,
        "column_summary": {},
    }

    for col in df.columns:
        col_data = df[col]
        summary = {
            "dtype": str(col_data.dtype),
            "null_count": col_data.isnull().sum(),
            "unique_values": col_data.nunique(),
        }

        if np.issubdtype(col_data.dtype, np.number):
            summary.update({
                "mean": col_data.mean(),
                "std": col_data.std(),
                "min": col_data.min(),
                "max": col_data.max(),
            })

        elif col_data.dtype == "object":
            summary.update({
                "top_values": col_data.value_counts().head(5).to_dict(),
            })

        desc_stats["column_summary"][col] = summary

    return desc_stats

def create_ydata_profile(df: pd.DataFrame, output_path: str = "outputs/generated_dashboards/ydata_profile.html"):
    profile = ydata_profiling.ProfileReport(df, title = "YData Profile Report", explorative = True)
    profile.to_file(output_path)
    return output_path

def create_sweetviz_report(df: pd.DataFrame, output_path: str = "outputs/generated_dashboards/sweetviz_report.html"):
    report = sweetviz.analyze(df)
    report.show_html(output_path, open_browser = False)
    return output_path

def extract_eda_insights(df: pd.DataFrame) -> list:
    insights = []
    if "sessions" in df.columns and "conversions" in df.columns:
        df["conversion_rate"] = df["conversions"] / df["sessions"]
        conv = df["conversion_rate"].mean()
        insights.append(f"Average conversion rate is {conv:.2%}.")

    if "device" in df.columns:
        top_device = df["device"].mode()[0]
        insights.append(f"Most traffic comes from: {top_device} users.")

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        peak_day = df.groupby("date")["sessions"].sum().idxmax()
        insights.append(f"Traffic peaked on {peak_day.strftime('%Y-%m-%d')}.")
    
    return insights

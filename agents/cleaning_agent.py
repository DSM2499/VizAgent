import pandas as pd
import janitor
import yaml
import os
from sklearn.impute import SimpleImputer
from io import StringIO
from datetime import datetime

def load_cleaning_rules(config_path = "config/cleaning_rules.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
    
def clean_data(df: pd.DataFrame, rules: dict) -> tuple[pd.DataFrame, str]:
    log = StringIO()
    log.write(f"Cleaning Log - {datetime.now()}\n")

    #Drop columns with too many nulls
    null_ratio = df.isnull().mean()
    to_drop = null_ratio[null_ratio > rules["drop_column_null_threshold"]].index
    df.drop(columns = to_drop, inplace = True)
    log.write(f"Dropped columns due to null threshold: {list(to_drop)}\n")

    #Remove duplicates
    if rules.get("remove_duplicates", True):
        before = len(df)
        df.drop_duplicates(inplace = True)
        after = len(df)
        log.write(f"Removed {before - after} duplicate rows\n")
    
    for col in df.columns:
        if df[col].dtype == object:
            sample_values = df[col].dropna().astype(str).head(20)
            if sample_values.str.match(r"^[\d\.,%\$ ]+$").mean() > 0.6:
                cleaned_col = (
                    df[col]
                    .astype(str)
                    .str.replace(r"[%\$,]", "", regex=True)
                    .str.replace(" ", "")
                )
                df[col] = pd.to_numeric(cleaned_col, errors="coerce")
                log.write(f"Converted string-like numbers to numeric in column '{col}'\n")


    #Convert date columns
    if rules.get("convert_dates", True):
        for col in df.columns:
            if df[col].dtype == "object":
                try:
                    df[col] = pd.to_datetime(df[col])
                    log.write(f"Converted {col} to datetime\n")
                except:
                    continue
    
    #Fill NA
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            strategy = rules["fillna_strategy"].get("numeric", "mean")
            if strategy == "mean":
                df[col].fillna(df[col].mean(), inplace = True)
            elif strategy == "median":
                df[col].fillna(df[col].median(), inplace = True)
            elif strategy == "mode":
                df[col].fillna(df[col].mode()[0], inplace = True)
        elif df[col].dtype == "object":
            strategy = rules["fillna_strategy"].get("categorical", "mode")
            if strategy == "mode":
                df[col].fillna(df[col].mode()[0], inplace = True)
                log.write(f"Filled NA in categorical column '{col}' with mode '{df[col].mode()[0]}'\n")
    
    return df, log.getvalue()
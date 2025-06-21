import pandas as pd
import duckdb
import polars as pl
import janitor
import chardet
import os

def detect_encoding(file_path, num_bytes = 10_000):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(num_bytes))
    return result['encoding']

def ingest_csv(file, use_duckdb = True):
    """
    Ingest and profile a CSV file using Duckdb or Polars. 
    Returns dataframe and metadata.
    """
    try:
        temp_path = f"data/sample_uploads/{file.name}"
        with open(temp_path, 'wb') as f:
            f.write(file.getbuffer())
        
        encoding = detect_encoding(temp_path)
        meta_data = {"filename": file.name, "encoding": encoding}

        if use_duckdb:
            df = duckdb.query(f"SELECT * FROM read_csv_auto('{temp_path}')").to_df()
        else:
            df = pl.read_csv(temp_path, encoding=encoding).to_pandas()
        

        meta_data.update({
            "n_rows": df.shape[0],
            "n_cols": df.shape[1],
            "columns": list(df.columns),
            "null_counts": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.apply(lambda x: str(x)).to_dict()
        })

        return df, meta_data
    except Exception as e:
        print(f"Error ingesting file {file.name}: {e}")
        return None, {"error": str(e)}
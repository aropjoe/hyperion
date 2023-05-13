import pandas as pd

def process_data(file_path):
    # Load data from CSV file
    df = pd.read_csv(file_path)
    
    # Clean data
    df['date'] = pd.to_datetime(df['date'])
    df = df.dropna()
    
    return df
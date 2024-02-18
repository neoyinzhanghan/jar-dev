import pandas as pd

def process_df(df):
    # Ensure 'Start Time' and 'End Time' are in datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Copy the DataFrame to avoid modifying the original data
    new_df = df.copy()
    
    # Calculate duration in minutes
    new_df["duration"] = (new_df["End Time"] - new_df["Start Time"]).dt.total_seconds() / 60
    
    # Extract date from 'Start Time'
    new_df["date"] = new_df["Start Time"].dt.date
    
    return new_df

def get_num_entries(df):
    """ Return the number of entries in the df """
    return len(df)
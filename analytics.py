import pandas as pd

def process_df(df):
    """ Calculate the following numbers as new columns for the df:
    - duration : End Time - Start Time in minutes 
    - date : the date of the event (without the time) """

    new_df = df.copy()
    new_df["duration"] = (df["End Time"] - df["Start Time"]).dt.total_seconds() / 60
    new_df["date"] = df["Start Time"].dt.date

    return new_df

def get_num_entries(df):
    """ Return the number of entries in the df """
    return len(df)
import pandas as pd

def merge_dataframes(dataframes):
    appended_df = pd.concat(dataframes)
    appended_df = appended_df.reset_index(drop=True)
 
    return appended_df
import pandas as pd
import numpy as np
def clean_dataframe(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    #indices_to_delete = df.isin([np.nan, np.inf, -np.inf]).any(1)
    
    return df[indices_to_keep].astype(np.float64)
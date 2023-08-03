import pandas as pd


# this file contains the base data on which we are performing operations , extracting data and getting insights

def preprocess(df,region_df):
    S_df = df[df['Season'] == "Summer"]

    # merge region df and   summer df
    S_df = S_df.merge(region_df, on='NOC', how='left')
    # one hot encoding medals
    S_df = pd.concat([S_df, pd.get_dummies(S_df['Medal'])],axis=1)
    return S_df



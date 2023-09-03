import pandas as pd

df_region = pd.read_csv("noc_regions.csv")

df_main = pd.read_csv("athlete_events.csv")

def preprocess():
    global df_region,df_main

    df_merge = df_main.merge(df_region, on="NOC", how="left")

    df_merge["Age"] = df_merge["Age"].fillna(df_merge["Age"].mode()[0])
    df_merge["Age"] = df_merge["Age"].astype("int64")
    df_merge["notes"] = df_merge["notes"].fillna("Missing")
    df_merge.drop_duplicates(inplace=True)
    df_merge["region"] = df_merge.apply(lambda x: x["Team"] if pd.isna(x["region"]) else x["region"], axis=1)

    medal_catg = pd.get_dummies(df_merge["Medal"])
    df_merge = pd.concat([df_merge, medal_catg], axis=1)
    df_merge = df_merge.drop(
        df_main[(df_main["NOC"] == "IND") * (df_merge["Season"] == "Winter") & (df_merge["Medal"] == "Gold")].index)
    return(df_merge)


def fetch_summer_medal_df(df_merge, years_s, country_s):
    medal_tally = df_merge.drop_duplicates(
        subset=["Team", "NOC", "Year", "Season", "Games", "City", "Sport", "Event", "Medal"])

    # Filter medal_tally DataFrame for Summer season
    summer_medal_df = medal_tally[medal_tally["Season"] == "Summer"]

    flag = 0
    if years_s == "Overall" and country_s == "Overall":
        fetch_summer_df = summer_medal_df
    if years_s == "Overall" and country_s != "Overall":
        flag = 1
        fetch_summer_df = summer_medal_df[summer_medal_df["region"] == country_s]
    if years_s != "Overall" and country_s == "Overall":
        fetch_summer_df = summer_medal_df[summer_medal_df["Year"] == int(years_s)]
    if years_s != "Overall" and country_s != "Overall":
        fetch_summer_df = summer_medal_df[
            (summer_medal_df["region"] == country_s) & (summer_medal_df["Year"] == int(years_s))]

    if flag == 1:
        df_summer = fetch_summer_df.groupby("Year").sum()[["Gold", "Silver", "Bronze"]].sort_values("Year",ascending=False).reset_index()
    else:
        df_summer = fetch_summer_df.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold",ascending=False).reset_index()

    df_summer['Gold'] = df_summer['Gold'].astype('int')
    df_summer['Silver'] = df_summer['Silver'].astype('int')
    df_summer['Bronze'] = df_summer['Bronze'].astype('int')

    return (df_summer)


def fetch_winter_medal_df(df_merge, years_w, country_w):
    medal_tally = df_merge.drop_duplicates(
        subset=["Team", "NOC", "Year", "Season", "Games", "City", "Sport", "Event", "Medal"])

    # Filter medal_tally DataFrame for Winter season
    winter_medal_df = medal_tally[medal_tally["Season"] == "Winter"]

    flag = 0
    if years_w == "Overall" and country_w == "Overall":
        fetch_winter_df = winter_medal_df
    if years_w == "Overall" and country_w != "Overall":
        flag = 1
        fetch_winter_df = winter_medal_df[winter_medal_df["region"] == country_w]
    if years_w != "Overall" and country_w == "Overall":
        fetch_winter_df = winter_medal_df[winter_medal_df["Year"] == int(years_w)]
    if years_w != "Overall" and country_w != "Overall":
        fetch_winter_df = winter_medal_df[
            (winter_medal_df["region"] == country_w) & (winter_medal_df["Year"] == int(year_w))]

    if flag == 1:
        df_winter = fetch_winter_df.groupby("Year").sum()[["Gold", "Silver", "Bronze"]].sort_values("Year",ascending=False).reset_index()
    else:
        df_winter = fetch_winter_df.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold",ascending=False).reset_index()

    return (df_winter)

def summer_year_country(df_merge):
    medal_tally = df_merge.drop_duplicates(
        subset=["Team", "NOC", "Year", "Season", "Games", "City", "Sport", "Event", "Medal"])

    # Filter medal_tally DataFrame for Summer season
    summer_medal_df = medal_tally[medal_tally["Season"] == "Summer"]
    years_s = summer_medal_df["Year"].unique().tolist()
    years_s.sort()
    years_s.insert(0, "Overall")

    country_s = summer_medal_df["region"].unique().tolist()
    country_s.sort()
    country_s.insert(0, "Overall")
    return years_s, country_s

def winter_year_country(df_merge):
    medal_tally = df_merge.drop_duplicates(
        subset=["Team", "NOC", "Year", "Season", "Games", "City", "Sport", "Event", "Medal"])

    # Filter medal_tally DataFrame for Winter season
    winter_medal_df = medal_tally[medal_tally["Season"] == "Winter"]
    years_w = winter_medal_df["Year"].unique().tolist()
    years_w.sort()
    years_w.insert(0, "Overall")

    country_w = winter_medal_df["region"].unique().tolist()
    country_w.sort()
    country_w.insert(0,"Overall")
    return years_w,country_w

def data_over_time_summer(df_merge,col):
    df_summer = df_merge[df_merge["Season"] == "Summer"]
    nations_over_time_s = df_summer[["Year", col]].drop_duplicates()
    nations_over_time_s = nations_over_time_s["Year"].value_counts().reset_index()
    nations_over_time_s.rename(columns={"index": "Year", "Year": col}, inplace=True)
    nations_over_time_s = nations_over_time_s.sort_values("Year", ascending=True)
    return nations_over_time_s

def data_over_time_winter(df_merge, col):
    df_winter = df_merge[df_merge["Season"] == "Winter"]
    nations_over_time_w = df_winter[["Year", col]].drop_duplicates()
    nations_over_time_w = nations_over_time_w["Year"].value_counts().reset_index()
    nations_over_time_w.rename(columns={"index": "Year", "Year": col}, inplace=True)
    nations_over_time_w = nations_over_time_w.sort_values("Year", ascending=True)
    return nations_over_time_w

def countrywise_medal_years(df_merge, country):
    df_summer = df_merge[df_merge["Season"] == "Summer"]
    df_summer.drop_duplicates(["Team", "Year", "Sport", "Event", "NOC", "Games", "City", "Medal"], inplace=True)
    country_medal_tally = df_summer.dropna(subset=["Medal"])
    country_medal_tally = country_medal_tally[country_medal_tally["region"] == country]
    country_medal_tally = country_medal_tally.groupby("Year").count()["Medal"].reset_index()
    return country_medal_tally

def country_sport_medals(df_merge, country):
    df_summer = df_merge[df_merge["Season"] == "Summer"]
    df_summer.drop_duplicates(["Team", "Year", "Sport", "Event", "NOC", "Games", "City", "Medal"], inplace=True)
    country_medal_tally = df_summer.dropna(subset=["Medal"])
    country_medal_tally = country_medal_tally[country_medal_tally["region"] == country]
    table = country_medal_tally.pivot_table(index="Sport", columns="Year", values="Medal", aggfunc='count').fillna(0)
    return table

def weight_height_ath(df_merge, sport):
    df_athlete = df_merge.drop_duplicates(["Name", "region"])
    df_athlete["Medal"].fillna("No medal", inplace=True)
    if (sport != "Overall"):
        x = df_athlete[df_athlete["Sport"] == sport]
        return x
    else:
        return df_athlete
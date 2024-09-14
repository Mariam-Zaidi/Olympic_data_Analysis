pip install --force-reinstall numpy pandas scikit-learn opencv-python
conda update numpy pandas scikit-learn opencv
import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

@st.cache
def load_noc_regions(nrows):
    data = pd.read_csv("noc_regions.csv")
    return data

@st.cache
def load_athlete_events(nrows):
    data = pd.read_csv("athlete_events.csv")
    return data


df_region = load_noc_regions(230)

df_main = load_athlete_events(271116)

df_merge = preprocessor.preprocess()
st.sidebar.title("Olympics Analysis (1896 - 2016)")
user_menu = st.sidebar.radio(
                    "Select one Option",
                    ("Medal Tally",
                     "Overall Analysis",
                     "Country-wise Analysis",
                     "Athlete-wise Analysis")
                    )

if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")
    medal_tally_subset = st.sidebar.radio("Select preferred season for Medal Tally",
                                  ("Summer","Winter")
                                  )
    if medal_tally_subset == "Summer":
        y,c = helper.summer_year_country(df_merge)

        selected_y = st.sidebar.selectbox("Select Year", y)
        selected_c = st.sidebar.selectbox("Select Country", c)

        summer_medal_tally = helper.fetch_summer_medal_df(df_merge,selected_y,selected_c)
        if selected_y == "Overall" and selected_c == "Overall":
            st.subheader("Overall Tally for Summer Olympics")
        if selected_y != "Overall" and selected_c == "Overall":
            st.subheader("Summer Olympics Medal tally for year " + str(selected_y))
        if selected_y == "Overall" and selected_c != "Overall":
            st.subheader(str(selected_c) + "'s overall performance in Summer Olympics")
        if selected_y != "Overall" and selected_c != "Overall":
            st.subheader(str(selected_c) + "'s Summer Olympics performance in year " + str(selected_y))
        st.table(summer_medal_tally)

    elif medal_tally_subset == "Winter":
        y, c = helper.winter_year_country(df_merge)

        selected_y = st.sidebar.selectbox("Select Year", y)
        selected_c = st.sidebar.selectbox("Select Country", c)

        winter_medal_tally = helper.fetch_winter_medal_df(df_merge,selected_y,selected_c)

        if selected_y == "Overall" and selected_c == "Overall":
            st.subheader("Overall Tally for Winter Olympics")
        if selected_y != "Overall" and selected_c == "Overall":
            st.subheader("Winter Olympics Medal tally for year " + str(selected_y))
        if selected_y == "Overall" and selected_c != "Overall":
            st.subheader(str(selected_c) + "'s overall performance in Winter Olympics")
        if selected_y != "Overall" and selected_c != "Overall":
            st.subheader(str(selected_c) + "'s Winter Olympics performance in year " + str(selected_y))
        st.table(winter_medal_tally)

if user_menu == "Overall Analysis":
    st.sidebar.header("Overall Analysis")
    overall_anly_subset = st.sidebar.radio("Select season for Overall Analysis",
                                           ("Summer", "Winter"))
    if overall_anly_subset == "Summer":
        medal_tally = df_merge.drop_duplicates(
            subset=["Team", "NOC", "Year", "Season", "Games", "City", "Sport", "Event", "Medal"])
        summer_medal_tally = medal_tally[medal_tally["Season"] == "Summer"]
        editions_s = summer_medal_tally["Year"].unique().shape[0]
        cities_s = summer_medal_tally["City"].unique().shape[0]
        events_s = summer_medal_tally["Event"].unique().shape[0]
        sports_s = summer_medal_tally["Sport"].unique().shape[0]
        athletes_s = summer_medal_tally["Name"].unique().shape[0]
        nations_s = summer_medal_tally["NOC"].unique().shape[0]

        st.title("Overall Analysis for Summer Olympics")
        col1,col2,col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions_s)
        with col2:
            st.header("Hosts")
            st.title(cities_s)
        with col3:
            st.header("Sports Events")
            st.title(events_s)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Sports")
            st.title(sports_s)
        with col2:
            st.header("Athletes")
            st.title(athletes_s)
        with col3:
            st.header("Nations")
            st.title(nations_s)

        nations_over_time_s = helper.data_over_time_summer(df_merge,"region")
        fig = px.line(nations_over_time_s, y="region", x="Year",
                      title="Participating Nations over years - Summer Olympics")
        st.plotly_chart(fig)

        events_over_time_s = helper.data_over_time_summer(df_merge,"Event")
        fig = px.line(events_over_time_s, y="Event", x="Year",
                      title="Events that took place over years - Summer Olympics")
        st.plotly_chart(fig)

        st.subheader("Number of Events organized per Sport over time")
        fig, ax = plt.subplots(figsize=(20, 20))
        df_summer = df_merge[df_merge["Season"] == "Summer"]
        sportwise_events_over_time_s = df_summer.drop_duplicates(["Sport", "Event", "Year"])
        table = sportwise_events_over_time_s.pivot_table(index="Sport", columns="Year", values="Event",
                                                         aggfunc="count").fillna(0).astype("int")
        ax = sns.heatmap(table, annot=True)
        st.pyplot(fig)

    if overall_anly_subset == "Winter":
        medal_tally = df_merge.drop_duplicates(
            subset=["Team", "NOC", "Year", "Season", "Games", "City", "Sport", "Event", "Medal"])
        winter_medal_tally = medal_tally[medal_tally["Season"] == "Winter"]
        editions_w = winter_medal_tally["Year"].unique().shape[0]
        cities_w = winter_medal_tally["City"].unique().shape[0]
        events_w = winter_medal_tally["Event"].unique().shape[0]
        sports_w = winter_medal_tally["Sport"].unique().shape[0]
        athletes_w = winter_medal_tally["Name"].unique().shape[0]
        nations_w = winter_medal_tally["NOC"].unique().shape[0]

        st.title("Overall Analysis for Winter Olympics")
        col1,col2,col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions_w)
        with col2:
            st.header("Hosts")
            st.title(cities_w)
        with col3:
            st.header("Sports Events")
            st.title(events_w)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Sports")
            st.title(sports_w)
        with col2:
            st.header("Athletes")
            st.title(athletes_w)
        with col3:
            st.header("Nations")
            st.title(nations_w)

        nations_over_time_w = helper.data_over_time_winter(df_merge, "region")
        fig = px.line(nations_over_time_w, y="region", x="Year",
                      title="Participating Nations over years - Winter Olympics")
        st.plotly_chart(fig)

        events_over_time_w = helper.data_over_time_winter(df_merge, "Event")
        fig = px.line(events_over_time_w, y="Event", x="Year",
                      title="Events that took place over years - Winter Olympics")
        st.plotly_chart(fig)

        st.subheader("Number of Events organized per Sport over time")
        fig,ax = plt.subplots(figsize = (20,20))
        df_winter = df_merge[df_merge["Season"] == "Winter"]
        sportwise_events_over_time_w = df_winter.drop_duplicates(["Sport", "Event", "Year"])
        table = sportwise_events_over_time_w.pivot_table(index="Sport", columns="Year", values="Event",
                                                         aggfunc="count").fillna(0).astype("int")
        ax = sns.heatmap(table, annot=True)
        st.pyplot(fig)

if user_menu == "Country-wise Analysis":

    st.sidebar.title("Country-wise Analysis")

    country_list = df_merge["region"].unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select Country", country_list)

    country_medal_tally = helper.countrywise_medal_years(df_merge, selected_country)
    st.subheader("Medals won by "+ selected_country+ " over the years")
    fig = px.bar(country_medal_tally, y="Medal", x="Year")
    st.plotly_chart(fig)

    table = helper.country_sport_medals(df_merge,selected_country)
    st.subheader( selected_country + " excels in the given sports over the years")
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(table, annot=True)
    st.pyplot(fig)

if user_menu == "Athlete-wise Analysis":

    df_athlete = df_merge.drop_duplicates(["Name", "region"])
    x1 = df_athlete["Age"]
    x2 = df_athlete[df_athlete["Medal"] == "Gold"]["Age"]
    x3 = df_athlete[df_athlete["Medal"] == "Silver"]["Age"]
    x4 = df_athlete[df_athlete["Medal"] == "Bronze"]["Age"]
    fig = ff.create_distplot([x1, x2, x3, x4], ["Overall Age", "Gold_Medal", "Silver_Medal", "Bronze_Medal"],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Probability of winning wrt Age")
    st.plotly_chart(fig)


    sports_list = df_merge["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "Overall")

    st.subheader("Height v/s Weight Analysis for each Sport")
    selected_sport = st.selectbox("Select Sport", sports_list)
    x = helper.weight_height_ath(df_merge, selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x["Height"], x["Weight"], hue=x["Medal"], style=x["Sex"], s=20, alpha = 0.7)
    st.pyplot(fig)

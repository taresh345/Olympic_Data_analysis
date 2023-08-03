import streamlit as st
import pandas as pd
import helper, preprocesser
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff




df=pd.read_csv('D://ML ineuron//olympic DATA analysis//archive//athlete_events.csv')
region_df=pd.read_csv("D://ML ineuron//olympic DATA analysis//archive//noc_regions.csv")

S_df=preprocesser.preprocess(df,region_df)

st.sidebar.header("OLYMPIC ANALYSIS")

user_menu = st.sidebar.radio(

    "SELECT AN OPTION",
    ('MEDAL TALLY', 'OVERALL ANALYSIS', 'COUNTRY WISE ANALYSIS', 'ATHLETE WISE ANALYSIS')
)


# ______________________________MEDAL TALLY_________________________________________________________________________________
if user_menu=="MEDAL TALLY":
    st.sidebar.header("MEDAL TALLY")
    years,country=helper.country_year_list(S_df)
    # years is a list of year
    #country is a list of countries
    selected_year=st.sidebar.selectbox("Select year",years) # will return one option
    selected_country=st.sidebar.selectbox("Select country",country)  # will return one option


    if selected_country=="Overall" and selected_year == "Overall":

        st.title("Overall tally")
    if selected_country!="Overall" and selected_year == "Overall":

        st.title(selected_country+" over the years")
    if selected_country=="Overall" and selected_year != "Overall":

        st.title("Overall tally in "+ str(selected_year))
    if selected_country!="Overall" and selected_year != "Overall":

        st.title("Tally of "+selected_country +" in the Year "+str(selected_year))

    medal_tally= helper.fetch_medaltally(selected_year,selected_country,S_df)
    st.table(medal_tally)




# ______________________________MEDAL TALLY__END____________________________________________________________________________




# ______________________________OVERALL ANALYSIS___________________________________________________________________________


if user_menu=='OVERALL ANALYSIS':

    st.sidebar.header("TOP STATISTICS")
    st.header("TOP STATISTICS")


    total_edition = S_df['Year'].nunique()
    total_cities = S_df['City'].nunique()
    total_sports = S_df['Sport'].nunique()
    total_event = S_df['Event'].nunique()
    total_athlete = S_df['Name'].nunique()
    total_country = S_df['region'].nunique()



    # create 3 columns
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("EDITIONS")
        st.title(total_edition)
    with col2:
        st.header("CITIES")
        st.title(total_cities)
    with col3:
        st.header("SPORTS")
        st.title(total_sports)

    # create 3 columns
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("EVENT")
        st.title(total_event)
    with col2:
        st.header("ATHLETES")
        st.title(total_athlete)
    with col3:
        st.header("COUNTRIES")
        st.title(total_country)

    # '__________________________________Years vs Participation nation'____________________
    nations_over_time=helper.data_over_time(S_df,"region")
    fig = px.line(nations_over_time, x="Edition", y="region", title='Years vs Participation nation')
    st.title("Participating nations over the years")
    st.plotly_chart(fig)

    # __________________________________'Years vs Events'__________________________________
    events_over_time=helper.data_over_time(S_df,"Event")
    fig = px.line(events_over_time, x="Edition", y='Event', title='Years vs Events')
    st.plotly_chart(fig)
    # __________________________________'Years vs no of Athletes'___________________________
    athletes_over_time=helper.data_over_time(S_df,"Name")

    athletes_over_time.rename(columns={"Name": "No.of Athletes"}, inplace=True)

    fig = px.line(athletes_over_time, x="Edition", y="No.of Athletes", title='Years vs no of Athletes')
    st.plotly_chart(fig)



    # __________________________________No of events with time ( By Every Sport)_____________

    st.title("No of events with time ( By Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    # Heatmap for no of events by sports
    x = S_df.drop_duplicates(subset=['Year', 'Sport', "Event"])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    # __________________________________Most succesfull Athletes_______________________________

    st.title("Most succesful Athletes")

    Sports_list = S_df.Sport.unique().tolist()
    Sports_list.sort()
    Sports_list.insert(0, 'Overall')
    selected_sport=st.selectbox('Select a Sport',Sports_list)

    a=helper.most_succesful(S_df,selected_sport)
    st.table(a)





# ______________________________OVERALL ANALYSIS___END________________________________________________________________________





#_____________________________COUNTRY WISE ANALYSIS___________________________________________________________________________


if user_menu == "COUNTRY WISE ANALYSIS":
    # _________________________________'Years vs number of medal per year(By country)_________

    st.sidebar.title('COUNTRY WISE ANALYSIS')
    country_list = S_df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0, 'Overall')
    selected_country = st.sidebar.selectbox('Select a Country', country_list)



    # 1__________________________________
    fig = px.line(helper.yearwise_medal_tally(selected_country, S_df), x="Year", y='Medal', title=selected_country+' over the years')
    st.plotly_chart(fig)



    # _#2_______year vs medal in diff sports(filter country)______________which countries are good at what sport ?____


    st.title(selected_country+' excels in the following sports')
    fig,ax = plt.subplots(figsize=(20,20))
    # Heatmap for year vs medals in different sports

    if selected_country!="Overall":
        pt=helper.country_event_heatmap(selected_country,S_df)
        ax=sns.heatmap(pt,annot=True)
        st.pyplot(fig)

    elif selected_country=="Overall":
        st.title("Select a country ")





    # _#3_______most succesful countrywise______________Top 10 athletes by any country ?_________

    st.title('Most successful athletes of '+selected_country)
    st.table(helper.succesful_athletes_bycountry(S_df, selected_country))






#_____________________________COUNTRY WISE ANALYSIS__END______________________________________________________________________







# ______________________________ATHLETE WISE  ANALYSIS________________________________________________________________________


if user_menu == "ATHLETE WISE ANALYSIS":

    #____1____________________

    athlete_df = S_df.drop_duplicates(subset=['Name', 'region'])

    x = [athlete_df['Age'].dropna(), athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna(),
         athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna(),
         athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()]

    fig = ff.create_distplot([x[0], x[1], x[2], x[3]],
                             ['Age Distribution', 'Gold medallist', 'Silver medallist', 'bronze medallist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    #____2_________pdf of all sports age(Gold medals only)___________
    famous_sports = S_df[S_df['Year'] == 2016].drop_duplicates('Sport')['Sport'].tolist()
    x = []  # ages
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport].reset_index()
        x.append(temp_df[temp_df['Sport'] == sport]['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of different Sports-Age(Gold medals winner only)')
    st.plotly_chart(fig)

    #____3_________scatterplot (height vs weight ) for any sport___________
    fig,ax = plt.subplots(figsize=(20,10))
    Sports_list = athlete_df.Sport.unique().tolist()
    Sports_list.sort()
    Sports_list.insert(0, 'Overall')

    st.title("Height vs Weight for any Sport")
    selected_sport=st.selectbox('Select a Sport',Sports_list)

    temp_df=helper.weight_vs_height(athlete_df,selected_sport)

    ax=sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=100)

    st.pyplot(fig)

    #____4_________scatterplot (height vs weight ) for any sport___________

    st.title("MEN VS WOMEN OVER THE YEARS")

    temp_df=helper.males_vs_female(S_df)
    fig = px.line(temp_df, x='Year', y=['Males', 'Females'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)



# ______________________________ATHLETE WISE  ANALYSIS__END_________________________________________________________________





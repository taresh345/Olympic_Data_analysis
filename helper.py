# import numpy as np

# S_df is the data set we are working on
# medal_tally is the base table for overall tally
# years and country are variables for chocies

# ______________________________Medal tally slectbox ___________________________________________________________________________

# _______1__________
def medal_tally(S_df):
    #  to count team medals as only one
    # to remove duplicate rows of specific columns ,
    # we are only removing duplicate entries of the same team (hockey has 11 players +reserve)
    # medal table does not have all the player names , just number of medal per country
    medal_tally = S_df.drop_duplicates(subset=['Team', "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])

    medal_tally = medal_tally.groupby('NOC').sum()[["Gold", "Silver", "Bronze"]].sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_tally['Total Medals'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    #  now it is very close to medal tally till 2016 olympics
    # there are still discrepancies which can be awarded to updated countries /obsolete countries  etc .
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total Medals'] = medal_tally['Total Medals'].astype('int')


    return medal_tally

# _______2__________

def country_year_list(S_df):
    years = S_df.Year.unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = S_df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


# _______3__________

def fetch_medaltally(years, country, S_df):
    medal_df = S_df.drop_duplicates(subset=['Team', "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    flag = 0
    temp_df=0
    x=0

    if years == "Overall" and country == "Overall":
        temp_df = medal_df
        flag = 0
    if years == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if years != "Overall" and country == "Overall":
        flag = 0
        temp_df = medal_df[medal_df['Year'] == int(years)]

    if years != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df['Year'] == int(years)) & (medal_df['region'] == country)]
        flag = 0



    if flag == 0:
        x=temp_df.groupby('region').sum()[["Gold","Silver","Bronze"]].sort_values(by=['Gold','Silver','Bronze'],
                                                                                  ascending=[False,False,False]).reset_index()

    elif flag == 1:
        x = temp_df.groupby('Year').sum()[["Gold", "Silver", "Bronze"]].sort_values("Year",
                                                                                          ascending=True).reset_index()

    x["Total Medals"] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total Medals'] = x['Total Medals'].astype('int')
    return x


# ______________________________Medal tally slectbox END___________________________________________________________________________


# ______________________________OVRALL ANALYSIS slectbox ___________________________________________________________________________

# _______1__________

def data_over_time(S_df,col):   #for graphs
    data_over_time = S_df.groupby(['Year'])[col].nunique()
    data_over_time = data_over_time.to_frame().reset_index()
    data_over_time.rename(columns={"Year": "Edition"}, inplace=True)

    return data_over_time



# _______2__________

# functon which filters the data by sports and tell which athlete won the most number no of medals
def most_succesful(S_df, sport):
    a=0
    if sport == "Overall":
        a = S_df.dropna(subset=['Medal']).groupby(['Name', 'Sport', 'region']).sum()[['Gold', 'Silver', 'Bronze']]

    if sport != "Overall":
        a = S_df[S_df['Sport'] == sport].dropna(subset=['Medal']).groupby(['Name', 'Sport', 'region']).sum()[
            ['Gold', 'Silver', 'Bronze']]

    a['Total'] = a['Gold'] + a['Silver'] + a['Bronze']
    a = a.drop(columns=['Gold', 'Silver', 'Bronze'])

    a = a.sort_values(by=['Total'], ascending=False).reset_index()
    a.rename(columns={'region': 'Country', 'Total': 'Medals'}, inplace=True)

    return a


# ______________________________OVRALL ANALYSIS slectbox end ___________________________________________________________________________





# ______________________________COUNTRY-WISE ANALYSIS slectbox  ___________________________________________________________________________
# function for number of medals over the years by a particular country
# _______1__________

def yearwise_medal_tally(country,S_df):
    temp=S_df.drop_duplicates(subset=['Team',"NOC","Games","Year","City","Sport","Event","Medal"])
    temp=temp.groupby(['region','Year']).count()[['Medal']].sort_values(by=['Year',],ascending=[False]).reset_index()
    return temp[temp['region']==country]



#number of medals per sport per year for any country
# _______2__________
def country_event_heatmap(country,S_df):
    a=S_df[S_df['region']==country].drop_duplicates(subset=['Team',"NOC","Games","Year","City","Sport","Event","Medal"]).dropna(subset=['Medal'])
    a=a.groupby(['Year','Sport']).count()['Medal'].reset_index()

    a=a.pivot_table(index='Sport',columns='Year',values='Medal').fillna(0).astype(int)

    return a



#_______most succesful countrywise______________Top 10 athletes by any country ?____
# _______3__________
def succesful_athletes_bycountry(S_df, country):
    a = S_df[S_df['region'] == country].dropna(subset=['Medal']).groupby(['Name', 'Sport']).count()[
        ['Medal']].sort_values(by=['Medal'], ascending=False).reset_index().head(10)

    a.rename(columns={'region': 'Country'}, inplace=True)

    return a

# ______________________________COUNTRY-WISE ANALYSIS slectbox END___________________________________________________________________________



# ______________________________ATHLETE ANALYSIS slectbox  ___________________________________________________________________________
# _______1__________
def weight_vs_height(athlete_df,sport):
    temp_df=0
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df=athlete_df[athlete_df['Sport']==sport]

    if sport == "Overall":
        temp_df=athlete_df

    return temp_df
# _______2__________
def males_vs_female(S_df):
    male=S_df[S_df['Sex']=='M'].groupby(by=['Year','Sex']).count()[['Name']].reset_index()
    female=S_df[S_df['Sex']=='F'].groupby(by=['Year','Sex']).count()[['Name']].reset_index()
    temp_df=male.merge(female,on='Year',how='left')
    temp_df.rename(columns={'Name_x':'Males',"Name_y":"Females"},inplace=True)
    temp_df.drop(columns=['Sex_x','Sex_y'],inplace=True)
    return temp_df


# ______________________________ATHLETE ANALYSIS slectbox END  ___________________________________________________________________________




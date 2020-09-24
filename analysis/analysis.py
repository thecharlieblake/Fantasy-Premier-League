import pandas as pd
import re

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt, isnan

# Load data
all_gameweek_df = pd.read_csv('analysis/all_gameweek_data.csv')
all_players_df = pd.read_csv('analysis/all_player_data.csv')

# Process / filter intial gameweek data
analysis_df = all_gameweek_df
name_regex = re.compile("(\D*)(:?_\d*)?$")  # Removes numbers at end of names for later seasons
analysis_df['name'] = analysis_df['name'].apply(lambda n: name_regex.search(n).group(1))
all_players_df['position'] = all_players_df['element_type'].apply(lambda i: ['GK', 'DEF', 'MID', 'FWD'][i-1])

team_map_18_19 = [
    'Arsenal', 'Bournemouth', 'Brighton', 'Burnley', 'Cardiff',
    'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Huddersfield',
    'Leicester', 'Liverpool', ' Man City', 'Man United', 'Newcastle',
    'Southampton', 'Tottenham', 'Watford', 'West Ham', 'Wolves'
]
analysis_df['opponent_team'] = analysis_df.loc[analysis_df['season'] == '2018-19']['opponent_team'].apply(lambda i: team_map_18_19[i-1])
all_players_df['team'] = all_players_df.loc[all_players_df['season'] == '2018-19']['team'].apply(lambda i: team_map_18_19[i-1])

gw_columns = ['element', 'season', 'name', 'total_points', 'round', 'minutes', 'opponent_team', 'was_home', 'value']
player_columns = ['id', 'season', 'position', 'team']

analysis_df = analysis_df.loc[:, gw_columns]
all_players_df = all_players_df.loc[:, player_columns]

# Join tables
analysis_df = pd.merge(analysis_df, all_players_df, how='left', left_on=['element','season'], right_on = ['id','season'])
analysis_df = analysis_df.drop(['element', 'id'], axis=1)

##################
# SETUP COMPLETE #
##################

analysis_2018_19 = analysis_df.loc[(analysis_df['season'] == '2018-19')]

a = analysis_2018_19.loc[analysis_2018_19['name'] == 'Gerard_Deulofeu', ['name', 'minutes', 'opponent_team', 'was_home', 'round',]]

a.to_csv('analysis/tmp.csv', index=False)



# Fabianski, dubravka, foster, schmeichel, patricio

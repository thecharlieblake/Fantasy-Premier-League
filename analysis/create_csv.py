import pandas as pd
import glob
import itertools

overall_df = pd.DataFrame()
players_overall_df = pd.DataFrame()
seasons = ['2016-17', '2017-18', '2018-19', '2019-20']

season_id = total_gw = 1
for season in seasons:
    players_file, ids_file = (glob.glob("data/" + season + f)[0] for f in ["/players_raw.csv", "/player_idlist.csv"])
    players_df, ids_df = (pd.read_csv(f, encoding = "ISO-8859-1") for f in [players_file, ids_file])
    players_df['season'] = season
    players_df['season_id'] = season_id

    players_df = players_df.drop(players_df[
                                     (players_df.first_name == 'Danny')
                                     & (players_df.second_name == 'Ward')
                                     & ((players_df.team_code == 13) | (players_df.team_code == 14))
                                     ].index)

    players_overall_df = players_overall_df.append(players_df, ignore_index=True)
    for w in range(38):
        gw = str(w + 1)
        gw_file = glob.glob("data/" + season + "/gws/gw" + gw + ".csv")[0]
        gw_df = pd.read_csv(gw_file, encoding = "ISO-8859-1")

        gw_df['season'] = season
        gw_df['season_id'] = season_id
        gw_df['gw'] = gw
        gw_df['total_gw'] = total_gw

        if 'id' in gw_df.columns:
            gw_df['id_old'] = gw_df['id']
            gw_df.drop('id', axis=1, inplace=True)

        for n in ["Danny_Ward", "Danny_Ward_457", "Danny_Ward_170"]:
            if n in gw_df['name'].unique():
                gw_df.drop(gw_df[gw_df['name'] == n].index, inplace=True)

        gw_df = pd.merge(gw_df, ids_df, left_on='element', right_on='id', how='left')
        gw_df = pd.merge(gw_df, players_df[['team_code', 'first_name', 'second_name']], on=['first_name', 'second_name'], how='left')
        overall_df = overall_df.append(gw_df, ignore_index=True)
        total_gw += 1
    season_id += 1

# cleanup
overall_df.dropna(axis=1, inplace=True)
overall_df.drop(['kickoff_time', 'id', 'name'], axis=1, inplace=True)

for c in overall_df.columns:
    if c not in ['season', 'creativity', 'ict_index', 'influence', 'first_name', 'second_name']:
        overall_df[c] = overall_df[c].astype(int)

overall_df['gw_match_no'] = 1
overall_df['double_gw'] = False
overall_df.loc[overall_df.duplicated(['element', 'total_gw'], keep='last'), 'gw_match_no'] = 2
overall_df.loc[overall_df.duplicated(['element', 'total_gw'], keep=False), 'double_gw'] = True

overall_df.drop(overall_df[(overall_df.season_id == 4) & (overall_df.gw == 29) & (overall_df.fixture == 275)].index, inplace=True)
overall_df.drop(overall_df[(overall_df.season_id == 2) & (overall_df.gw == 22) & (overall_df.fixture == 220) & (overall_df.element == 449)].index, inplace=True)
overall_df.drop(overall_df[(overall_df.season_id == 2) & (overall_df.gw == 22) & (overall_df.fixture == 219) & (overall_df.element == 392)].index, inplace=True)

tmp = overall_df[['team_code', 'season_id', 'gw', 'gw_match_no']]\
    .sort_values(['team_code', 'season_id', 'gw', 'gw_match_no']).drop_duplicates()
tmp2 = tmp.groupby(['team_code', 'season_id']).agg(['count'])
assert tmp2[tmp2['gw', 'count'] != 38].sum()[0] == 0
tmp['season_game'] = list(itertools.chain.from_iterable([list(range(1, 38 + 1)) for x in range(len(seasons) * 20)]))
overall_df = pd.merge(overall_df, tmp, on=['team_code', 'season_id', 'gw', 'gw_match_no'], how='left')

name_idxs = ['second_name', 'first_name']
names = overall_df[name_idxs].drop_duplicates().sort_values(name_idxs)
names['player_id'] = list(range(1, len(names.index) + 1))
overall_df = pd.merge(overall_df, names, on=name_idxs, how='left')
overall_df = overall_df.set_index(['season_id', 'gw', 'gw_match_no', 'team_code', 'player_id']).sort_index()

overall_df.to_csv('analysis/all_gameweek_data.csv', index=False)
players_overall_df.to_csv('analysis/all_player_data.csv', index=False)
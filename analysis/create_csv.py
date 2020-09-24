import pandas as pd
import glob

overall_df = pd.DataFrame()
players_overall_df = pd.DataFrame()


season_idx = gw_idx = 0
for season in ['2016-17', '2017-18', '2018-19', '2019-20']:
    players_file = glob.glob("data/" + season + "/players_raw.csv")[0]
    players_df = pd.read_csv(players_file, encoding = "ISO-8859-1")
    players_df['season'] = season
    players_df['season_idx'] = season_idx
    players_overall_df = players_overall_df.append(players_df, ignore_index=True)
    for w in range(38):
        gw = str(w + 1)
        gw_file = glob.glob("data/" + season + "/gws/gw" + gw + ".csv")[0]
        gw_df = pd.read_csv(gw_file, encoding = "ISO-8859-1")
        gw_df['season'] = season
        gw_df['season_idx'] = season_idx
        gw_df['gw'] = gw
        gw_df['gw_idx'] = gw_idx
        overall_df = overall_df.append(gw_df, ignore_index=True)
        gw_idx += 1
    season_idx += 1

# cleanup
overall_df.dropna(inplace=True)
overall_df.drop(['kickoff_time', 'kickoff_time_formatted', 'ea_index'], axis=1, inplace=True)

for c in overall_df.columns:
    if c not in ['name', 'season', 'creativity', 'ict_index', 'influence']:
        overall_df[c] = overall_df[c].astype(int)

overall_df.to_csv('analysis/all_gameweek_data.csv', index=False)
players_overall_df.to_csv('analysis/all_player_data.csv', index=False)
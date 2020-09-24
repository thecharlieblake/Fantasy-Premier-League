import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

df = pd.read_csv('analysis/all_gameweek_data.csv', encoding="ISO-8859-1")

#%% cleanup
df = df.set_index(['season_id', 'gw', 'gw_match_no', 'team_code', 'player_id']).sort_index()


#%% data overview
df.info()

#%% test
print("test")
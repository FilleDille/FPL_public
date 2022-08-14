import long_to_short_team
import pandas as pd
import sys

dict_shortname = long_to_short_team.dict

def get(home, away):
    dict = {
        'home_offence':df_home_off_pivot.loc[home, away], 
        'home_defence':df_home_def_pivot.loc[home, away],
        'away_offence':df_away_off_pivot.loc[home, away],
        'away_defence':df_away_def_pivot.loc[home, away]
        }
    
    return dict

def main():
    df_all = pd.read_csv(main_csv)
    df_all['team_x'] = df_all['team_x'].str.upper().map(dict_shortname)
    df_all['opp_team_name'] = df_all['opp_team_name'].str.upper().map(dict_shortname)
    df_all.dropna(axis=0, inplace=True)

    df_all['home_offence'] = df_all.apply(lambda x:get(x['team_x'], x['opp_team_name'])['home_offence'], axis=1)
    df_all['home_defence'] = df_all.apply(lambda x:get(x['team_x'], x['opp_team_name'])['home_defence'], axis=1)
    df_all['away_offence'] = df_all.apply(lambda x:get(x['team_x'], x['opp_team_name'])['away_offence'], axis=1)
    df_all['away_defence'] = df_all.apply(lambda x:get(x['team_x'], x['opp_team_name'])['away_defence'], axis=1)

    to_drop = ['Unnamed: 0', 'season_x', 'assists',
        'bonus', 'clean_sheets', 'creativity', 'element', 'fixture',
        'goals_conceded', 'goals_scored', 'influence',
        'kickoff_time', 'minutes', 'opponent_team',
        'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards',
        'round', 'saves', 'selected', 'team_a_score', 'team_h_score', 'threat', 
        'transfers_balance', 'transfers_in', 'transfers_out', 'was_home', 'yellow_cards', 'GW']

    df_all = df_all.drop(to_drop, axis=1)

    df_all = df_all[['name', 'team_x', 'opp_team_name', 'bps', 'ict_index',
        'value', 'home_offence', 'home_defence', 'away_offence', 'away_defence',
        'position', 'total_points']]

    export_name = 'training_data_nodummies.csv'
    
    df_all.to_csv(export_name) 

    print(f'Export lyckad, se {export_name}')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <main csv file> <fdr csv file>. Eg: python {sys.argv[0]} main_data.csv fdr.csv")
        sys.exit(1)

    main_csv = sys.argv[1]
    fdr_csv = sys.argv[2]

    df_fdr = pd.read_csv(fdr_csv, sep=';')
    df_fdr.drop(['id', 'event', 'finished', 'team_home', 'team_away'], axis=1, inplace=True)

    df_home_off_pivot = df_fdr.pivot(index='team_home_name', columns='team_away_name', values='team_h_rank_offence')
    df_home_def_pivot = df_fdr.pivot(index='team_home_name', columns='team_away_name', values='team_h_rank_defence')
    df_away_off_pivot = df_fdr.pivot(index='team_home_name', columns='team_away_name', values='team_a_rank_offence')
    df_away_def_pivot = df_fdr.pivot(index='team_home_name', columns='team_away_name', values='team_a_rank_defence')

    main()
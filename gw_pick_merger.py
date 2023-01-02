import os
import pandas as pd
import glob
import sys


def main(gw_min: int, gw_max: int):
    gw_files = glob.glob(os.getcwd() + '/**/gw*.csv', recursive=True)
    picks_files = glob.glob(os.getcwd() + '/**/picks*.csv', recursive=True)
    df_gw = pd.DataFrame()
    df_picks = pd.DataFrame()

    gw_files = list(filter(lambda x: x.split('/gw')[1].split('.csv')[0].isnumeric() and gw_min <= int(x.split('/gw')[1].split('.csv')[0]) <= gw_max, gw_files))

    for gw in gw_files:
        df_temp = pd.read_csv(gw)
        df_gw = pd.concat([df_gw, df_temp], ignore_index=True)

    picks_files = list(filter(lambda x: gw_min <= int(x.split('/picks_')[1].split('.csv')[0]) <= gw_max, picks_files))

    for pick in picks_files:
        df_temp = pd.read_csv(pick)
        df_temp['team_id'] = pick.split('team_')[1].split('_data')[0]
        df_temp['round'] = pick.split('picks_')[1].split('.csv')[0]
        df_picks = pd.concat([df_picks, df_temp], ignore_index=True)

    df_picks.drop(['position', 'is_captain', 'is_vice_captain'], axis=1, inplace=True)

    df_picks['round'] = df_picks['round'].astype(str)
    df_gw['round'] = df_gw['round'].astype(str)
    df_gw['total_points'] = df_gw['total_points'].astype(float)

    df_temp = df_gw.groupby('name')['influence'].rolling(5).mean()
    df_temp = df_temp.reset_index().set_index('level_1')
    df_gw['influence_rolling'] = df_temp['influence']

    df_temp_2 = df_gw.groupby('name')['bps'].rolling(5).mean()
    df_temp_2 = df_temp_2.reset_index().set_index('level_1')
    df_gw['bps_rolling'] = df_temp_2['bps']

    df_gw['bps_influence'] = df_gw['influence_rolling'] + df_gw['bps_rolling']
    df_gw['xP_delta'] = df_gw['total_points'] - df_gw['xP']

    df_merged = pd.merge(df_picks, df_gw, on=['element', 'round'], how='inner')

    df_merged['multiplied_points'] = df_merged['multiplier'] * df_merged['total_points']
    df_merged['multiplied_delta'] = df_merged['multiplied_points'] - (df_merged['multiplier'] * df_merged['xP_delta'])
    df_merged['multiplied_delta'] = df_merged['multiplied_delta'].astype(float)

    export_name = f'df_merged_{gw_min}_{gw_max}_incl_calc.csv'

    df_gw.to_csv(export_name, index=False)
    print(f'DataFrame successfully exported as {export_name}')


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <gw_min> <gw_max>. Eg: python {sys.argv[0]} 1 11")
        sys.exit(1)

    main(int(sys.argv[1]), int(sys.argv[2]))
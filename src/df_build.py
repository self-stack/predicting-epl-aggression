import numpy as np
import pandas as pd

def csv_to_df():
    '''
    Creates df from csv's. Adds season tracker (1-10). Pulls pertinent game statistics

    
    Returns
    ----------
    game_stats: (DataFrame)
        DataFrame of 10 season csv's.
    '''
    season_18_19 = pd.read_csv('../data/premier_league/season-1819_csv.csv')
    season_17_18 = pd.read_csv('../data/premier_league/season-1718_csv.csv')
    season_16_17 = pd.read_csv('../data/premier_league/season-1617_csv.csv')
    season_15_16 = pd.read_csv('../data/premier_league/season-1516_csv.csv')
    season_14_15 = pd.read_csv('../data/premier_league/season-1415_csv.csv')
    season_13_14 = pd.read_csv('../data/premier_league/season-1314_csv.csv')
    season_12_13 = pd.read_csv('../data/premier_league/season-1213_csv.csv')
    season_11_12 = pd.read_csv('../data/premier_league/season-1112_csv.csv')
    season_10_11 = pd.read_csv('../data/premier_league/season-1011_csv.csv')
    season_09_10 = pd.read_csv('../data/premier_league/season-0910_csv.csv')
    seasons = [season_18_19, season_17_18, season_16_17, season_15_16, season_14_15, 
                season_13_14, season_12_13, season_11_12, season_10_11, season_09_10]
    
    season_num = 'Season'

    # add season tracker
    for i, s in enumerate(seasons[::-1]):
        s[season_num] = i + 1

    ten_season_df = pd.concat(seasons)

    stat_features = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 
                'HTAG', 'HTR', 'Referee', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 
                'AC', 'HY', 'AY', 'HR', 'AR', 'Season']

    described_features = ['Date', 'HomeTeam', 'AwayTeam', 'Final_Goals_H', 'Final_Goals_A',
                'Final_Result', 'Half_Goals_H', 'Half_Goals_A', 'Half_Result', 'Referee',
                'Shots_H', 'Shots_A', 'Target_Shots_H', 'Target_Shots_A', 'Fouls_H',
                'Fouls_A', 'Corners_H', 'Corners_A', 'Yellow_H', 'Yellow_A', 'Red_H',
                'Red_A', 'Season']
    
    # generate game_stats df, index and chrono order with Data field
    game_stats = ten_season_df[stat_features]
    game_stats.Date = pd.to_datetime(game_stats.Date)
    game_stats.set_index(game_stats['Date'], inplace=True)
    game_stats.columns = described_features
    # clean game_stats df and del ten_season_df & seasons df to release memory
    game_stats.pop('Date')
    game_stats.pop('Half_Goals_H')
    game_stats.pop('Half_Goals_A')
    game_stats.pop('Half_Result')
    game_stats.pop('Referee')
    del ten_season_df
    del seasons

    return game_stats


def df_team_focus(df, team):
    '''
    Creates data frame of team vs. opponent stats.


    Parameters
    ----------
    df: (DataFrame)
        Season DataFrame to analyze
    team: (string)
        Team name to build df.


    Returns
    ----------
    df_feature_engineering(team_focus): (Function)
        Passes team_focus to df_feature_engineering. Returns resulting engineering feature DataFrame
    '''

    team_home = df[df.HomeTeam == team]
    team_away = df[df.AwayTeam == team]
    # dummyise H/A/D seperately to handle W/L
    team_home, team_away = dummyize_match_results(team_home, team_away)
    team_focus = pd.concat([team_home, team_away])
    team_focus.Home_Final_D.fillna(0, inplace=True)
    team_focus.Away_Final_D.fillna(0, inplace=True)
    team_focus.Home_Final_H.fillna(0, inplace=True)
    team_focus.Away_Final_A.fillna(0, inplace=True)
    # add draw, away+home wins cols together; convert to int
    team_focus['draw'] = team_focus.Home_Final_D + team_focus.Away_Final_D
    team_focus['win'] = team_focus.Home_Final_H + team_focus.Away_Final_A
    team_focus.draw = team_focus.draw.astype(dtype='int64')
    team_focus.win = team_focus.win.astype(dtype='int64')

    team_focus['Home_Field_Advantage'] = np.where(team_focus.HomeTeam == team, 1, 0)
    team_focus.Home_Field_Advantage = team_focus.Home_Field_Advantage.astype(dtype='bool')
    team_focus['opponent'] = np.where(team_focus.Home_Field_Advantage, team_focus.AwayTeam, team_focus.HomeTeam)


    # del 
    team_focus.pop('Final_Result')
    team_focus.pop('Home_Final_H')
    team_focus.pop('Away_Final_A')
    team_focus.pop('Home_Final_D')
    team_focus.pop('Away_Final_D')
    del team_home
    del team_away
    
    return df_feature_organization(team_focus)


def dummyize_match_results(home, away):
    '''
    Dummy-izes Final Result for home and away seperately.


    Parameters
    ----------
    away: (DataFrame)
        DataFrame of when provided team is away team.
    
    home: (DataFrame)
        DataFrame of when provided team is home team.


    Returns
    ----------
    away: (DataFrame)
        DataFrame of when provided team is away team.
    
    home: (DataFrame)
        DataFrame of when provided team is home team.
    '''
    home_final_dummies = pd.get_dummies(home.Final_Result, prefix='Home_Final')
    away_final_dummies = pd.get_dummies(away.Final_Result, prefix='Away_Final')
    home = pd.concat([home, home_final_dummies], axis=1)
    away = pd.concat([away, away_final_dummies], axis=1)

    # del
    home.pop('Home_Final_A')
    away.pop('Away_Final_H')

    return home, away


def df_feature_organization(df):
    '''
    Creates data frame of team vs. opponent stats.


    Parameters
    ----------
    df: (DataFrame)
        DataFrame focused on team in question.


    Returns
    ----------
    df: (DataFrame)
        DataFrame of when provided team is away team.
    '''
    col_list = ['season_num', 'draw', 'win', 'home_advan', 'opponent', 'team_goals', 'oppon_goals',
            'team_shots', 'oppon_shots', 'team_target_shots', 'oppon_target_shots', 'team_fouls', 'oppon_fouls',
            'team_corners', 'oppon_corners', 'team_yellows', 'oppon_yellows', 'team_reds', 'oppon_reds']
    
    org_col_list = ['home_advan', 'team_shots', 'team_target_shots', 'team_goals', 'team_fouls', 'team_corners', 
            'team_yellows', 'team_reds', 'opponent', 'oppon_shots', 'oppon_target_shots', 'oppon_goals', 
            'oppon_fouls', 'oppon_corners', 'oppon_yellows', 'oppon_reds', 'season_num']

    # goals
    df['team_goals'] = np.where(df.Home_Field_Advantage, df.Final_Goals_H, df.Final_Goals_A)
    df['oppon_goals'] = np.where(~df.Home_Field_Advantage, df.Final_Goals_H, df.Final_Goals_A)
    #shots
    df['team_shots'] = np.where(df.Home_Field_Advantage, df.Shots_H, df.Shots_A)
    df['oppon_shots'] = np.where(~df.Home_Field_Advantage, df.Shots_H, df.Shots_A)
    # target shots
    df['team_target_shots'] = np.where(df.Home_Field_Advantage, df.Target_Shots_H, df.Target_Shots_A)
    df['oppon_target_shots'] = np.where(~df.Home_Field_Advantage, df.Target_Shots_H, df.Target_Shots_A)
    # fouls
    df['team_fouls'] = np.where(df.Home_Field_Advantage, df.Fouls_H, df.Fouls_A)
    df['oppon_fouls'] = np.where(~df.Home_Field_Advantage, df.Fouls_H, df.Fouls_A)
    # corners
    df['team_corners'] = np.where(df.Home_Field_Advantage, df.Corners_H, df.Corners_A)
    df['oppon_corners'] = np.where(~df.Home_Field_Advantage, df.Corners_H, df.Corners_A)
    # yellows
    df['team_yellows'] = np.where(df.Home_Field_Advantage, df.Yellow_H, df.Yellow_A)
    df['oppon_yellows'] = np.where(~df.Home_Field_Advantage, df.Yellow_H, df.Yellow_A)
    # reds
    df['team_reds'] = np.where(df.Home_Field_Advantage, df.Red_H, df.Red_A)
    df['oppon_reds'] = np.where(~df.Home_Field_Advantage, df.Red_H, df.Red_A)


    # del
    df.pop('HomeTeam')
    df.pop('AwayTeam')
    df.pop('Final_Goals_H')
    df.pop('Final_Goals_A')
    df.pop('Shots_H')
    df.pop('Shots_A')
    df.pop('Target_Shots_H')
    df.pop('Target_Shots_A')
    df.pop('Fouls_H')
    df.pop('Fouls_A')
    df.pop('Corners_H')
    df.pop('Corners_A')
    df.pop('Yellow_H')
    df.pop('Yellow_A')
    df.pop('Red_H')
    df.pop('Red_A')

    df.columns = col_list
    #sort datetime index
    df = df.sort_index()[::-1]


    return df[org_col_list] 
import pandas as pd
import numpy as np
import os

def csv_to_df():
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

    for i, s in enumerate(seasons[::-1]):
        s[season_num] = i + 1

    ten_season_df = pd.concat(seasons)

    stat_features = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 
                'HTAG', 'HTR', 'Referee', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 
                'AC', 'HY', 'AY', 'HR', 'AR', 'Season']

    described_features = ['HomeTeam', 'AwayTeam', 'Final_Goals_H', 'Final_Goals_A',
                'Final_Result', 'Half_Goals_H', 'Half_Goals_A', 'Half_Result', 'Referee',
                'Shots_H', 'Shots_A', 'Target_Shots_H', 'Target_Shots_A', 'Fouls_H',
                'Fouls_A', 'Corners_H', 'Corners_A', 'Yellow_H', 'Yellow_A', 'Red_H',
                'Red_A', 'Season']
    
    game_stats = ten_season_df[stat_features]
    game_stats.Date = pd.to_datetime(game_stats.Date)
    game_stats.set_index(game_stats['Date'], inplace=True)
    game_stats.drop(['Date'], axis=1, inplace=True)
    game_stats.columns = described_features
    game_stats.drop(['Half_Goals_H','Half_Goals_A', 'Half_Result','Referee'],
            axis=1, inplace=True)

    return game_stats, game_stats.HomeTeam.unique()

def team_record_df_build(df, team):
    '''
    Creates data frame with engineered features based on team passed in.


    Parameters
    ----------
    df: (DataFrame)
        Season DataFrame to analyze
    team: (string)
        Team name to build df.


    Returns
    ----------
    away_df: (DataFrame)
        DataFrame of when provided team is away team.
    
    home_df: (DataFrame)
        DataFrame of when provided team is home team.
    '''
    team_home = df[df.HomeTeam == team]
    team_away = df[df.AwayTeam == team]

    print('\n{0} W/L/D Distribution Season \'09-\'17'.format(team))
    total_wins = np.sum(team_home[team_home.Season <=8].Final_Result == 'H') + np.sum(team_away[team_away.Season <=8].Final_Result == 'A')
    total_loss = np.sum(team_home[team_home.Season <=8].Final_Result == 'A') + np.sum(team_away[team_away.Season <=8].Final_Result == 'H')
    total_draw = np.sum(team_home[team_home.Season <=8].Final_Result == 'D') + np.sum(team_away[team_away.Season <=8].Final_Result == 'D')
    print('''
    Team Win Percentage: {0:0.2f}%
    Team Loss Percentage: {1:0.2f}%
    Team Draw Percentage: {2:0.2f}%'''.format((total_wins/len(team_home+team_away))*100, 
                                            (total_loss/len(team_home+team_away))*100,
                                            (total_draw/len(team_home+team_away))*100))


def model_prep():
    pass
    





if __name__ == '__main__':
    df, team_options = csv_to_df()
    team_selection_prompt='\n\nSelect a team from the options below:'
    team_selected = False
    
    while not team_selected:
        print(team_selection_prompt)
        print(team_options)
        team = input('>>>')

        if team in team_options:
            team_record_df_build(df, team)
            another = input('\nWould you like to view anothe team? (y/n)')

            if another == 'y':
                continue
            else:
                print('Goodbye!')
                team_selected = True
        else:
            print('\nTry Again\n')
            continue

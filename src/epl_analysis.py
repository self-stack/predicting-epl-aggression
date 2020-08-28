import df_build as build
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.metrics import confusion_matrix

def rf_model(df):
    '''
    Model prep and run to predict if game will have a red flag.


    Parameters
    ----------
    df: (DataFrame)
        Full record of team in analysis.
    '''
    game_to_predict = '2019-10-02'
    model_data = team_focus.copy()
    # construct target feature
    y = model_data.pop('team_reds')
    y = y[y.index < game_to_predict]
    y.shift()
    y_train, y_test = y[100:], y[:100]
    # construct model data
    X = model_data.drop(['opponent', 'season_num'], axis=1)
    home_flag = X.pop('home_advan')
    X = X.sort_index().rolling(3).mean()
    X = X.sort_index()[::-1]
    X.insert(0, 'home_advan', home_flag)
    X_train, X_test = X[100:-2], X[:100]
    
    # predictive model
    bal_rf = BalancedRandomForestClassifier()
    bal_rf.fit(X_train, y_train)

    # model metric
    print('Scoring OOB: {0}'.format(bal_rf.score(X_test, y_test)))

    y_predict = bal_rf.predict(X_test)
    print('Confusion Matrix: {0}'.format(y_test, y_predict))







if __name__ == '__main__':
    season_20_21_team_options = ['Arsenal', 'Aston Villa', 'Brighton', 'Burnley',
    'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Leicester', 'Liverpool',
    'Man City', 'Man United', 'Newcastle', 'Southhampton', 'Tottenham', 'West Brom',
    'West Ham', 'Wolves']

    df = build.csv_to_df()
    team_selection_prompt='\n\nSelect a team from the options below:'
    team_selected = False
    
    while not team_selected:
        print(team_selection_prompt)
        print(season_20_21_team_options)
        # TODO: MAKE team GLOBAL VARIABLE
        team = input('>>>')

        if team in season_20_21_team_options:
            record = build.df_team_focus(df, team)

            another = input('\nWould you like to view another team? (y/n)')

            if another == 'y':
                continue
            else:
                print('Goodbye!')
                team_selected = True
        else:
            print('\nTry Again\n')
            continue

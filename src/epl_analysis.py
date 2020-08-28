import df_build as build
from sklearn.metrics import confusion_matrix, precision_score, recall_score


def eda(df, team):
    #  keep as bool??
    # df.home_field_advantage = dfd.home_Field_Advantage.astype(dtype='int64')
    pass
    
def rf_model(df):
    # sklearn.model_selection.TimeSeriesSplit??
    train, test = df[df.season_num <=8], df[df.season_num > 8]
    # pop season_num, drop in assignement to keep for eda tracking?
    y_train, y_test = train.pop('home_reds'), test.pop('home_reds')
    X_train, X_test = train.values, test.values
    
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    print('Score: {0:0.2f}'.format(rf.score(X_test, y_test)*100))
    y_predict = rf.predict(X_test)
    print('Confusion Matrix:')
    print(confusion_matrix(y_test, y_predict))






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
        # MAKE team GLOBAL VARIABLE
        team = input('>>>')

        if team in season_20_21_team_options:
            record = build.df_team_focus(df, team)
            record.info()

            another = input('\nWould you like to view another team? (y/n)')

            if another == 'y':
                continue
            else:
                print('Goodbye!')
                team_selected = True
        else:
            print('\nTry Again\n')
            continue

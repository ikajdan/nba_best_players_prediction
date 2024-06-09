import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from processing.plotting import plot_feature_importance


def predict_top_players(rookies=False):
    """
    Predict the top NBA players for the 2024 season

    Args:
    rookies (bool): Whether to predict rookies or non-rookies

    Returns:
    list: List of predicted top NBA players
    """

    nba_data = pd.read_csv("./data/nba_data.csv")

    if rookies:
        players = nba_data[nba_data["RK"] == 1]
        y = players["ANBARK"]
    else:
        players = nba_data[nba_data["RK"] == 0]
        y = players["ANBA"]

    features = [
        "VORP",
        "WS",
        "OWS",
        "BPM",
        "OBPM",
        "USG%",
        "PER",
        "DWS",
        "MP",
        "WS/48",
    ]

    # features = players.drop(
    #     columns=["Player", "Pos", "ANBA", "ANBARK", "RK"]
    # ).columns.tolist()

    X = players[features]
    X = pd.get_dummies(X)

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.02, random_state=12)
    model = RandomForestClassifier(n_estimators=200, random_state=21)
    model.fit(X_train, y_train)

    # plot_feature_importance(model, X.columns)

    nba_data_2024 = pd.read_csv("./data/nba_data_2024.csv")

    if rookies:
        players_2024 = nba_data_2024[nba_data_2024["RK"] == 1]
    else:
        players_2024 = nba_data_2024[nba_data_2024["RK"] == 0]

    X_2024 = players_2024[features]
    X_2024 = pd.get_dummies(X_2024)

    predictions = model.predict(X_2024)
    predicted_players = players_2024[predictions == 1]["Player"].tolist()

    # with open("./model.pkl", "wb") as model_file:
    #     pickle.dump(model, model_file)

    return predicted_players

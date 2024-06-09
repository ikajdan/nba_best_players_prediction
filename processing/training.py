# import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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

    # Split data into rookies and non-rookies
    rookies = nba_data[nba_data["RK"] == 1].drop(columns=["RK"])
    non_rookies = nba_data[nba_data["RK"] == 0].drop(columns=["RK"])

    # Features to be used in the model based on the feature importance
    selected_features = [
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

    # Or use all features
    # selected_features = non_rookies.drop(
    #     columns=["Player", "Pos", "ANBA", "ANBARK"]
    # ).columns.tolist()

    y = non_rookies["ANBA"]
    X = non_rookies[selected_features]
    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.02, random_state=12
    )

    model = RandomForestClassifier(n_estimators=200, random_state=21)
    model.fit(X_train, y_train)

    # predictions = model.predict(X_test)
    # accuracy = accuracy_score(y_test, predictions)
    # print(f"Model Training Accuracy: {accuracy:.2f}")

    nba_data_2024 = pd.read_csv("./data/nba_data_2024.csv")

    rookies_2024 = nba_data_2024[nba_data_2024["RK"] == 1].drop(columns=["RK"])
    non_rookies_2024 = nba_data_2024[nba_data_2024["RK"] == 0].drop(columns=["RK"])

    X_2024 = non_rookies_2024[selected_features]
    X_2024 = pd.get_dummies(X_2024)

    predictions_2024 = model.predict(X_2024)
    predicted_players = non_rookies_2024[predictions_2024 == 1]["Player"].tolist()

    # plot_feature_importance(model, X.columns)

    # y_2024 = non_rookies_2024["ANBA"]
    # accuracy_2024 = accuracy_score(y_2024, predictions_2024)
    # print(f"Model Testing Accuracy: {accuracy_2024:.2f}")

    # print(
    #     f"Predicted All-NBA players: {non_rookies_2024[predictions_2024 == 1]['Player'].tolist()}"
    # )
    # print(f"Actual All-NBA players: {non_rookies_2024[y_2024 == 1]['Player'].tolist()}")
    # print(f"Predicted All-NBA players count: {predictions_2024.sum()}")

    # with open("./model.pkl", "wb") as model_file:
    #     pickle.dump(model, model_file)

    return predicted_players

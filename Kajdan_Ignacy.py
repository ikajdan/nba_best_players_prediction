import argparse
import json
from pathlib import Path

from processing.training import predict_top_players


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_file", type=str)
    args = parser.parse_args()

    results_file = Path(args.results_file)

    predicted_players = predict_top_players(rookies=False)
    predicted_rookies = predict_top_players(rookies=True)
    json_data = {
        "first all-nba team": predicted_players[:5],
        "second all-nba team": predicted_players[5:10],
        "third all-nba team": predicted_players[10:15],
        "first rookie all-nba team": predicted_rookies[:5],
        "second rookie all-nba team": predicted_rookies[5:10],
    }

    with results_file.open("w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

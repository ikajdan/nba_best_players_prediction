import matplotlib.pyplot as plt
import numpy as np


def plot_feature_importance(model, feature_names):
    """
    Plot the feature importance of the model

    Args:
    model (object): Trained model

    feature_names (list): List of feature names

    Returns:
    None
    """
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importance")
    plt.bar(range(len(importances)), importances[indices], align="center")
    plt.xticks(range(len(importances)), np.array(feature_names)[indices], rotation=90)
    plt.xlabel("Features")
    plt.ylabel("Importance Score")
    plt.tight_layout()
    plt.show()

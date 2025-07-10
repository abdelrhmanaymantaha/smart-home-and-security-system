import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from intent_model import SmartHomeIntentModel

def plot_classification_report(report):
    intents = [intent for intent in report.keys() if intent not in ["accuracy", "macro avg", "weighted avg"]]
    
    precision = [report[intent]["precision"] for intent in intents]
    recall = [report[intent]["recall"] for intent in intents]
    f1_score = [report[intent]["f1-score"] for intent in intents]

    x = np.arange(len(intents))  # Label locations
    width = 0.25  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - width, precision, width, label="Precision", color="royalblue")
    ax.bar(x, recall, width, label="Recall", color="seagreen")
    ax.bar(x + width, f1_score, width, label="F1-score", color="tomato")

    ax.set_xlabel("Intents")
    ax.set_ylabel("Scores")
    ax.set_title("Classification Report Metrics")
    ax.set_xticks(x)
    ax.set_xticklabels(intents, rotation=20)
    ax.legend()

    plt.ylim(0, 1.1)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

# Example usage
df = SmartHomeIntentModel().load_data()  # Load the dataset
report = SmartHomeIntentModel().train(df)  # Train the model and get the classification report
plot_classification_report(report)  # Plot the classification report

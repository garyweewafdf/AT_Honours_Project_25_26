import numpy as np
import joblib
import sys
import re
import math
import matplotlib.pyplot as plt

def test_model(model_path, scaler_path, frf_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    X_frf = np.load(frf_path)
    X_frf_scaled = scaler.transform(X_frf)
    predictions = model.predict(X_frf_scaled)

    results = ""
    for win, res in enumerate(predictions):
        if res == 1:
            results += f"Window {win:04d} : Normal\n"
        else:
            results += f"Window {win:04d} : Anomaly\n"

    total = len(predictions)
    normal = (predictions == 1).sum()
    anomalies = (predictions == -1).sum()

    if total > 0:
        anomaly_rate = anomalies / total 
    else: 
        anomaly_rate = 0

    print("\nSummarised Results")
    print(f"    Total Windows: {total}")
    print(f"    Normal:        {normal}")
    print(f"    Anomalies:     {anomalies}")
    print(f"    Anomaly Rate:  {anomaly_rate:.4f} ({anomaly_rate*100:.2f}%)")

    return results

def calculate(results):
    def is_true_anomaly(window_number):
        return (
            127 <= window_number <= 154 or
            240 <= window_number <= 277
        )

    TP = TN = FP = FN = 0
    for line in results.splitlines():
        match = re.search(r"Window\s+(\d+)\s+:\s+(Normal|Anomaly)", line)
        if not match:
            continue

        window = int(match.group(1))
        predicted = match.group(2)
        actual_is_anomaly = is_true_anomaly(window)

        if predicted == "Anomaly":
            predicted_is_anomaly = True
        else:
            predicted_is_anomaly = False

        if actual_is_anomaly and predicted_is_anomaly:
            TP += 1
        elif not actual_is_anomaly and not predicted_is_anomaly:
            TN += 1
        elif not actual_is_anomaly and predicted_is_anomaly:
            FP += 1
        elif actual_is_anomaly and not predicted_is_anomaly:
            FN += 1

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 / ((1 / precision) + (1 / recall))
    mcc = ((TP * TN) - (FP * FN)) / math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))

    return (TP, TN, FP, FN, accuracy, precision, recall, f1, mcc)

def output(TP, TN, FP, FN, accuracy, precision, recall, f1, mcc):
    print("\n------------------------")
    print(f"True Positives : {TP}")
    print(f"True Negatives : {TN}")
    print(f"False Positives: {FP}")
    print(f"False Negatives: {FN}\n")
    print(f"Accuracy: {100*accuracy:.2f}%")
    print(f"Precision: {100*precision:.2f}%")
    print(f"Recall: {100*recall:.2f}%")
    print(f"F1 Score: {100*f1:.2f}%")
    print(f"MCC Score: {100*mcc:.2f}%")

def visualise(accuracy, precision, recall, f1, mcc):
    metrics = {
        "Accuracy": accuracy * 100,
        "Precision": precision * 100,
        "Recall": recall * 100,
        "F1 Score": f1 * 100,
        "MCC": mcc * 100
    }

    plt.figure(figsize=(8, 6))
    bars = plt.bar(metrics.keys(), metrics.values())

    plt.ylabel("Percentage (%)")
    plt.title("Model Performance Metrics")
    plt.ylim(0, 110)
    plt.xticks(rotation=45)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1, 
            f"{height:.2f}%",
            ha='center',
            va='bottom'
        )

    plt.tight_layout()
    plt.show()

def confusion_matrix_plot(TP, TN, FP, FN):

    cm = [[TP, FN],
          [FP, TN]]

    labels = ["Anomaly", "Normal"]
    actual = ["Anomaly", "Normal"]

    plt.figure()
    plt.imshow(cm, cmap="Blues")

    for i in range(2):
        for j in range(2):
            plt.text(j, i, cm[i][j],
                     ha="center",
                     va="center",
                     color="black")

    plt.xticks([0,1], labels)
    plt.yticks([0,1], actual)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.colorbar()
    plt.tight_layout()
    plt.show()

def main():
    model_path = sys.argv[1]
    scaler_path = sys.argv[2]
    frf_path = sys.argv[3]

    results = test_model(model_path, scaler_path, frf_path)
    (TP, TN, FP, FN, accuracy, precision, recall, f1, mcc) = calculate(results)
    output(TP, TN, FP, FN, accuracy, precision, recall, f1, mcc)
    visualise(accuracy, precision, recall, f1, mcc)
    confusion_matrix_plot(TP, TN, FP, FN)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <model> <scaler> <FRF-processed>")
        sys.exit()
    main()

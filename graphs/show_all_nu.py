import numpy as np
import joblib
import math
import re
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from sklearn.svm import OneClassSVM

if len(sys.argv) != 4:
    print("python3 test_all_nu_.py [scaled training dataset (npg)] [un-scaled testing dataset (npy)] [scaler (pkl)]")
    sys.exit()

train_dataset = sys.argv[1]
frf_dataset = sys.argv[2]
scaler_path = sys.argv[3]

# Load datasets
X_train = np.load(train_dataset)
X_frf = np.load(frf_dataset)

print(f"[Training Dataset]          Min: {X_train.min()}    | Max: {X_train.max()}")
print(f"[Testing Dataset ]          Min: {X_frf.min()}                  | Max: {X_frf.max()}")

# Load scaler
scaler = joblib.load(scaler_path)

X_frf_scaled = scaler.transform(X_frf)

nu_values = []
accuracy_vals = []
precision_vals = []
recall_vals = []
f1_vals = []
mcc_vals = []

def calculate(results):

    def is_true_anomaly(window):
        return (
            127 <= window <= 154 or
            240 <= window <= 277
        )

    TP = TN = FP = FN = 0

    for line in results.splitlines():

        match = re.search(r"Window\s+(\d+)\s+:\s+(Normal|Anomaly)", line)
        if not match:
            continue

        window = int(match.group(1))
        predicted = match.group(2)

        actual_is_anomaly = is_true_anomaly(window)
        predicted_is_anomaly = predicted == "Anomaly"

        if actual_is_anomaly and predicted_is_anomaly:
            TP += 1
        elif not actual_is_anomaly and not predicted_is_anomaly:
            TN += 1
        elif not actual_is_anomaly and predicted_is_anomaly:
            FP += 1
        elif actual_is_anomaly and not predicted_is_anomaly:
            FN += 1

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = 2 / ((1/precision) + (1/recall)) if precision and recall else 0

    denom = math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    mcc = ((TP*TN)-(FP*FN))/denom if denom else 0

    return TP, TN, FP, FN, accuracy, precision, recall, f1, mcc


print("\nNU Sweep Results")
print("NU | Accuracy | Precision | Recall | F1 | MCC | TP | TN | FP | FN")

for nu in np.arange(0.01,1.00,0.01):

    model = OneClassSVM(kernel='rbf', gamma='scale', nu=nu)

    model.fit(X_train)

    predictions = model.predict(X_frf_scaled)

    results = ""
    for win,res in enumerate(predictions):
        if res == 1:
            results += f"Window {win:04d} : Normal\n"
        else:
            results += f"Window {win:04d} : Anomaly\n"

    TP,TN,FP,FN,accuracy,precision,recall,f1,mcc = calculate(results)

    print(f"{nu:.2f} | {accuracy*100:.2f}% | {precision*100:.2f}% | {recall*100:.2f}% | {f1*100:.2f}% | {mcc*100:.2f}% | {TP} | {TN} | {FP} | {FN}")

    nu_values.append(nu)
    accuracy_vals.append(accuracy)
    precision_vals.append(precision)
    recall_vals.append(recall)
    f1_vals.append(f1)
    mcc_vals.append(mcc)


def metric_graph_each(accuracy_vals, precision_vals, recall_vals, f1_vals, mcc_vals):
    metrics = {
        "Accuracy": accuracy_vals,
        "Precision": precision_vals,
        "Recall": recall_vals,
        "F1": f1_vals,
        "MCC": mcc_vals
    }

    for name,values in metrics.items():
        plt.figure()
        plt.plot(nu_values,[v*100 for v in values])
        plt.xlabel("Nu")
        plt.ylabel("Score (%)")
        plt.title(f"{name} vs Nu")
        plt.ylim(0,100)

        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(0.2))
        ax.xaxis.set_minor_locator(MultipleLocator(0.01))

        plt.xlim(0.01,1.00)
        plt.ylim(0,100)

        plt.grid(which='major', linestyle='-', linewidth=0.8)
        plt.grid(which='minor', linestyle=':', linewidth=0.5)

        plt.legend()
        plt.tight_layout()
        plt.show()

def metric_graph_all(accuracy_vals, precision_vals, recall_vals, f1_vals, mcc_vals):
    plt.figure(figsize=(10,6))
    plt.plot(nu_values, [v*100 for v in accuracy_vals], label="Accuracy")
    plt.plot(nu_values, [v*100 for v in precision_vals], label="Precision")
    plt.plot(nu_values, [v*100 for v in recall_vals], label="Recall")
    plt.plot(nu_values, [v*100 for v in f1_vals], label="F1 Score")
    plt.plot(nu_values, [v*100 for v in mcc_vals], label="MCC")
    plt.xlabel("Nu Value")
    plt.ylabel("Score (%)")
    plt.title("One-Class SVM Nu Hyperparameter Performance Evaluation")

    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.xaxis.set_minor_locator(MultipleLocator(0.01))

    plt.xlim(0.01,1.00)
    plt.ylim(0,100)

    plt.grid(which='major', linestyle='-', linewidth=0.8)
    plt.grid(which='minor', linestyle=':', linewidth=0.5)

    plt.legend()
    plt.tight_layout()
    plt.show()

metric_graph_each(accuracy_vals, precision_vals, recall_vals, f1_vals, mcc_vals)
metric_graph_all(accuracy_vals, precision_vals, recall_vals, f1_vals, mcc_vals)

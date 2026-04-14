import sys
import numpy as np
import joblib
from sklearn.svm import OneClassSVM
from datetime import datetime

dataset = sys.argv[1]
print(f"[+] Training Model Using {dataset}")
print(f"[/] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
x = np.load(dataset)

print(f"[+] Dataset shape: {x.shape}")

model = OneClassSVM(
    kernel='rbf',
    gamma='scale',  
    nu=0.01          
)

model.fit(x)

print("[+] Training complete")
print(f"[/] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
model_output = "trained_model.pkl"
joblib.dump(model, model_output)

print(f"[+] Model saved as: {model_output}")


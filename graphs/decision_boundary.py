import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.decomposition import PCA

# ----------------------------------------------------
# FILE PATHS
# ----------------------------------------------------
TRAIN_DATA = ""  # scaled
TEST_DATA = ""               # unscaled
MODEL_FILE = "" # saved model
SCALER_FILE = "" # scaler

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------
X_train_scaled = np.load(TRAIN_DATA)
X_test_unscaled = np.load(TEST_DATA)

model = joblib.load(MODEL_FILE)
scaler = joblib.load(SCALER_FILE)

# ----------------------------------------------------
# APPLY SCALING TO TEST DATA (matches evaluation step)
# ----------------------------------------------------
X_test_scaled = scaler.transform(X_test_unscaled)

# ----------------------------------------------------
# PCA FIT ONLY ON TRAINING DATA
# ----------------------------------------------------
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# ----------------------------------------------------
# MODEL PREDICTIONS (same as experiment)
# ----------------------------------------------------
y_pred = model.predict(X_test_scaled)
total_anomalies = (y_pred == -1).sum()
total_normal = (y_pred == 1).sum()

# ----------------------------------------------------
# CREATE GRID IN PCA SPACE
# ----------------------------------------------------
X_all_pca = np.vstack((X_train_pca, X_test_pca))
x_min, x_max = X_all_pca[:, 0].min() - 1, X_all_pca[:, 0].max() + 1
y_min, y_max = X_all_pca[:, 1].min() - 1, X_all_pca[:, 1].max() + 1

xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 400),
    np.linspace(y_min, y_max, 400)
)

grid_2d = np.c_[xx.ravel(), yy.ravel()]

# ----------------------------------------------------
# MAP BACK TO ORIGINAL (SCALED) FEATURE SPACE
# ----------------------------------------------------
grid_scaled = pca.inverse_transform(grid_2d)

# ----------------------------------------------------
# DECISION FUNCTION (REAL MODEL)
# ----------------------------------------------------
Z = model.decision_function(grid_scaled)
Z = Z.reshape(xx.shape)

# ----------------------------------------------------
# PLOT
# ----------------------------------------------------
plt.figure(figsize=(10, 8))

# Background: decision function
contour = plt.contourf(xx, yy, Z, levels=50, cmap="RdYlGn", alpha=0.6)
plt.colorbar(contour, label="Decision Function Value")

# Decision boundary
plt.contour(xx, yy, Z, levels=[0], colors="black", linewidths=2)

# Plot predictions
plt.scatter(
    X_test_pca[y_pred == 1, 0],
    X_test_pca[y_pred == 1, 1],
    c="green", s=20, label="Predicted Normal"+" ("+str(total_normal)+")"
)

plt.scatter(
    X_test_pca[y_pred == -1, 0],
    X_test_pca[y_pred == -1, 1],
    c="red", s=20, label="Predicted Anomaly"+" ("+str(total_anomalies)+")"
)

plt.title("RBF One-Class SVM Decision Boundary (Testing Data)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Honours Project 2025–2026

## Project Title
Securing The SDN Control Channel Against Man-in-The-Middle Attacks: Utilising One-Class Support Vector Machines For Detection

## Project Aim
The aim of this project is to develop and evaluate a One-Class Support Vector Machine (OC-SVM) model for detecting Flow-Rule Forgery (FRF) attacks within a Software-Defined Networking (SDN) environment.

## Repository Overview
This repository contains all code developed and used to achieve the stated project aim. 
The project focuses on training a OC-SVM model for FRF attack detection.

### Project Replication
To replicate the project, the required scripts are listed below in order of exeuction:

| # | Execution Stage             | Script(s)                                          | Script Purpose                                                            |
|---|-----------------------------|----------------------------------------------------|---------------------------------------------------------------------------|
| 1 | Gather training dataset     | `tcpdump` or `Wireshark`                           | Gather benign SDN control plane traffic (no anomalies)                    |
| 2 | Process training dataset    | `OC-SVM/Training/process_training_dataset.py`      | Process training dataset                                                  |
| 3 | Train OC-SVM model          | `OC-SVM/Training/train_model.py`                   | Train OC-SVM model with RBF kernel tuning and save model state            |
| 4 | Gather testing dataset      | `FRF/XXX`                                          | Execute FRF Attack (tool availability limitied to project markers only)   |
|   |                             | `tcpdump` or `Wireshark`                           | Capture SDN control plane traffic during FRF attack                       |
| 5 | Process testing dataset     | `OC-SVM/Testing/process_testing_dataset.py`        | Process testing dataset                                                   |
| 6 | Test OC-SVM model           | `OC-SVM/Testing/test_model.py`                     | Evaluate OC-SVM detection performance (with scaling applied)              |
|   |                             | `OC-SVM/Testing/show_all_nu.py`                    | Evaluate detection performance across nu values (0.00–1.00)               |

**Anomalous windows: 127-154 & 240-277**
* identified by noting time of FRF attack execution and corresponding time for each window: `OC-SVM/Testing/determine_window.py`  

To replicate all visual graphs included within the final report, below are the utilised programs:

| Script(s)                                | Script Purpose                                                              |
|------------------------------------------|-----------------------------------------------------------------------------|
| `graphs/decision_boundary.py`            | Display learned model boundary using training and testing datasets          |
| `graphs/protocol_distribution_visual.py` | Show protocol distribution percentages in datasets                          |
| `graphs/show_features.py`                | Display feature rates per window in processed datasets                      |
| `graphs/traffic_volume_visual.py`        | Compare traffic volume between training and testing datasets                |

#### Replication Data
The datasets and model artefacts used in this project are provided to enable direct replication of results without requiring retraining or data collection:
- `replication_data/datasets/processed_training_dataset.npy` – Processed training dataset  
- `replication_data/datasets/processed_testing_dataset.npy` – Processed testing dataset
- `replication_data/datasets/scaler.pkl` – Training scaler 
- `replication_data/datasets/trained_model.pkl` – Trained model state (model tuning: RBF, nu: 0.01, gamma: scale)

## Ethical Use Notice (FRF Attack Tool)
To uphold ethical and legal standards:
* The developed FRF attack tool is **NOT** included within this respository to uphold ethical and legal standards. Tool access is only granted for project markers, available on request.
* The FRF attack tool is strictly for educational and research purposes. Myself, the author, does not condone or support any malicious use of this tool.
* To ensure safe and responsible use, the tool must only be executed within controlled, isolated environments where all devices and network components are owned and governed by the user.

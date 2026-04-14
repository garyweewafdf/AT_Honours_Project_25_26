# Results
## Experimental Setup
### Processing Techniques 
* Feature Scaling: Standardisation (Z-Score)
* Feature Selection (Traffic rate): FlowMod, PACKET_IN, PACKET_OUT, ARP, TCP, Forwarding

### Model Configuration (OC-SVM Tuning) 
* Kernel: Radial Basis Function (RBF)
* Gamma: Scale
* Nu: 0.01

### Network Topology
<p align="left"> <img src="images/topology.png" width="700">  </p>

## Hyperparameter Analysis (nu) 
- `graphs/show_all_nu.py`:
<p align="left"> <img src="images/nu_values_tested.png" width="700">  </p>

## Model Performance
- `OC-SVM/Testing/test_model.py`:
<p align="left"> <img src="images/confusion_matrix.png" width="700">  </p>
<p align="left"> <img src="images/model_performance.png" width="700"> </p>

## Decision Boundary
- `graphs/decision_boundary.py`:
<p align="left"> <img src="images/learned_boundary.png" width="700">  </p>

## Dataset Analysis
### Traffic Volume Comparison
- `graphs/traffic_volume_visual.py`:
<p align="left"> <img src="images/traffic_volume_compare.png" width="700">  </p>

### Protocol Distribution
- `graphs/protocol_distribution_visual.py`:
<p align="left"> <img src="images/protocol_distribution_training.png" width="700"> </p>
<p align="left"> <img src="images/protocol_distribution_testing.png" width="700">  </p>

## Feature Behaviour
- `graphs/show_features.py`:
<p align="left"> <img src="images/feature_behaviour_training.png" width="700">  </p>
<p align="left"> <img src="images/feature_behaviour_testing.png" width="700"> </p>


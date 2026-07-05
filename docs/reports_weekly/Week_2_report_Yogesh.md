# Week 2 Report - Yogeshwaran
## Contextual Data Fusion and Feature Engineering

### Day 1 - External Context Simulation
- Simulated Ambient_temperature using normal distribution (mean=295K, std=3)
- Simulated Load_density using uniform distribution (0.3 to 1.0)
- Used random seed(42) for reproducibility
- Created fusion features:
  - temperature_gap = Air temp - Ambient temp
  - load_stress = power x Load_density

### Day 2 - Feature Validation
- Checked correlation of all 8 engineered features with Target
- Best feature: power (0.176)
- None beat original Torque (0.19) individually
- Created effective_power feature - scored 0.145

### Day 3 - Ablation Study
- Model A (5 original sensors): Macro F1 = 0.679
- Model B (5 sensors + 8 features): Macro F1 = 0.693
- Improvement of 0.014 proves features help!
- Added StandardScaler to fix convergence warning

### Day 4 - Timestamp Based Fusion
- Added timestamp using pd.date_range
- One reading per minute
- Time range: Jan 1 to Jan 8 (7 days)
- Final dataset: 16 columns

### Summary
- External context simulated and merged
- Ablation study proves 0.014 improvement
- GitHub commits: 13
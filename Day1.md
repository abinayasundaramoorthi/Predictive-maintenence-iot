# Day 1 External Context Research

1. Research: Ambient Temperature Data

Ambient temperature refers to the surrounding environmental temperature where industrial
machines operate. It is a critical external factor because thermal stress significantly affects machine
wear, lubrication viscosity, and component lifespan.
1.1 Why Ambient Temperature Matters
• High ambient temperature raises machine operating temperature beyond safe limits
• Low temperature increases lubrication viscosity, causing higher torque and wear
• Temperature swings cause material expansion/contraction leading to fatigue
• Extreme heat accelerates bearing degradation and tool wear in CNC machines
1.2 Realistic Temperature Ranges for Industrial Environments
Environment Type Temperature Range
(°C)
Notes
Factory floor (general) 18°C – 35°C Standard indoor industrial setting
Summer peak (India) 28°C – 42°C May–June in North India
(Uttarakhand region)
Winter low (India) 5°C – 18°C December–January in hilly
industrial areas
Night shift 15°C – 25°C Cooler due to reduced solar gain
Near heat-generating
machines
30°C – 50°C Furnaces, welding zones

2. Research: Factory Load Factors

Load density (or load factor) represents the operational demand placed on a machine at any given
time. Machines operating at near-maximum capacity for extended periods are at significantly higher
risk of failure.
2.1 Why Load Factors Matter
• Higher load means more mechanical stress on bearings, gears, and cutting tools
• Sustained high load prevents thermal recovery between operations
• Load spikes can trigger sudden failures even in well-maintained machines
• Low load operation after high-load periods can reveal latent damage
2.2 Load Factor Categories
Load Category Load Density Value Machine State Description
Idle 0.0 – 0.2 Machine running but no active job
Light Load 0.2 – 0.4 Below-capacity operation, warm-up phase
Normal Load 0.4 – 0.7 Standard production operation
Heavy Load 0.7 – 0.9 Near-capacity, high-demand production
run
Peak / Overload 0.9 – 1.0 Maximum capacity, risk of failure increases
2.3 Load Pattern Observations
• Morning shift (6am–2pm): load ramps up gradually from idle to normal
• Afternoon shift (2pm–10pm): peak production, highest load density
• Night shift (10pm–6am): reduced load, maintenance windows, cooldown
• Monday mornings and post-maintenance: typically start at low load

3. Defined Context Variables

Based on the research above, the following external context variables are defined for integration
with the AI4I Predictive Maintenance Dataset:
Variable Name Data Type Range / Values Description
ambient_temperature Float 5.0 – 45.0 (°C) Simulated environmental
temperature using sine wave +
noise
load_density Float 0.0 – 1.0 Normalized machine operational
load (0=idle, 1=max)
shift_type String morning /
afternoon / night
Production shift derived from
timestamp index
temp_diff Float Computed Difference: process_temp -
ambient_temperature
load_adjusted_torque Float Computed torque * load_density
(engineered feature)
thermal_load_index Float Computed ambient_temp * load_density
(combined stress indicator)
Note: The first three variables are raw external context features. The last three are engineered
features derived by combining external and internal sensor data.

4. Integration Plan

The following plan outlines how external context data will be created, merged, and validated before
use in predictive modeling.
4.1 Step-by-Step Integration Plan
Step Task Output Owner Task
Step 1 Load AI4I dataset and
extract row count + index
Base dataframe
(10,000 rows)
#40
Step 2 Generate synthetic
ambient_temperature
column
ambient_temp CSV #41
Step 3 Generate synthetic
load_density + shift_type
column
load_density CSV #42
Step 4 Validate both datasets:
range checks, nulls,
consistency
Validation report #43
Step Task Output Owner Task
Step 5 Merge external datasets
with AI4I on row index /
timestamp
Merged dataframe Week 2 final
Step 6 Engineer derived features
(temp_diff,
load_adjusted_torque)
Feature-rich
dataframe
Week 2 final
Step 7 Ablation study: compare
model accuracy with/without
features
Ablation report Week 2 final
4.2 Data Merge Strategy
• AI4I dataset has 10,000 rows — all synthetic data will also have exactly 10,000 rows
• Merge method: pd.concat or direct column assignment (index-aligned)
• No timestamp column in AI4I — row index acts as the time proxy
• Assume each row = 1 minute of machine operation for shift calculation
4.3 Tools & Libraries
• Python 3.x with pandas, numpy, matplotlib, seaborn
• scikit-learn for model training in ablation study
• Jupyter Notebook for interactive development and visualization

5. Document Findings

5.1 Key Research Findings
• Ambient temperature directly correlates with machine failure risk — high temperatures
increase thermal failures (HDF) probability
• Load density is the strongest predictor of mechanical failures (PWF, OSF) alongside torque
and rotational speed
• Combined features (temp * load) provide stronger signal than either feature alone
• Shift-based patterns reveal that afternoon shifts have the highest failure rate due to
sustained load
• Synthetic data generation using sine waves + Gaussian noise is widely accepted in
academic predictive maintenance research
5.2 Expected Impact on Model Performance
Feature Added Expected Model
Improvement
Failure Type Most Affected
ambient_temperature Moderate (+2–4% F1) Heat Dissipation Failure (HDF)
load_density High (+4–7% F1) Power/Overstrain Failure (PWF,
OSF)
shift_type Low-Moderate (+1–2%
F1)
All failure types
temp_diff (engineered) High (+3–5% F1) HDF, TWF
load_adjusted_torque
(engineered)
High (+5–8% F1) PWF, OSF, TWF
thermal_load_index
(engineered)

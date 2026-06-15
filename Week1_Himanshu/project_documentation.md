============================================================
AI4I PREDICTIVE MAINTENANCE DATASET - DOCUMENTATION
============================================================

1. DATA DICTIONARY
----------------------------------------
Dataset Name  : AI4I 2004 Predictive Maintenance Dataset
Total Rows    : 10000
Total Columns : 14

2. COLUMN DESCRIPTIONS
----------------------------------------
1. UDI
   - Unique identifier for each machine record

2. Product ID
   - Product quality type (L = Low, M = Medium, H = High)

3. Air Temperature [K]
   - Surrounding air temperature of the machine
   - Min: 295.3
   - Max: 304.5
   - Average: 300.0

4. Process Temperature [K]
   - Temperature generated during machining process
   - Min: 305.7
   - Max: 313.8
   - Average: 310.01

5. Rotational Speed [RPM]
   - How fast the motor is spinning per minute
   - Min: 1168
   - Max: 2886
   - Average: 1538.78

6. Torque [Nm]
   - Rotational force applied by the motor
   - Min: 3.8
   - Max: 76.6
   - Average: 39.99

7. Tool Wear [min]
   - How long the cutting tool has been in use
   - Min: 0
   - Max: 253
   - Average: 107.95

8. Machine Failure
   - Target column: 0 = Normal, 1 = Failed
   - Total Normal : 9661
   - Total Failed : 339

3. FAILURE TYPE DESCRIPTIONS
----------------------------------------
TWF - Tool Wear Failure
   - Happens when tool is used beyond its limit
   - Total Cases: 46

HDF - Heat Dissipation Failure
   - Happens when machine overheats
   - Total Cases: 115

PWF - Power Failure
   - Happens due to power supply problems
   - Total Cases: 95

OSF - Overstrain Failure
   - Happens when machine is overloaded
   - Total Cases: 98

RNF - Random Failure
   - Unexpected random failure
   - Total Cases: 19

4. BUSINESS NOTES
----------------------------------------
- Machine failures are RARE (highly imbalanced dataset)
- Early failure prediction can save huge maintenance costs
- Failed machines show higher torque and tool wear on average
- Goal: Predict failure BEFORE it happens
- Target Metric: Macro F1 Score >= 0.85




# WeightWise
WeightWise 1.7
 
 
 
WeightWise v1.7 is a PyQt5-based desktop application designed to help users track their weight loss or gain journey, estimate water retention, and manage health goals. The application features an interactive user interface where users can input their current weight, set target weight goals, and track their progress over time. The app also considers factors such as water retention based on lifestyle inputs, including diet and physical activity levels.

Features
Weight Tracking: Input your daily weight records and monitor progress towards your target weight.
Water Retention Estimation: Estimate water retention based on factors like salt intake, carbohydrate consumption, and physical activity levels.
Target Weight: Set and track your target weight to measure your success.
Data Persistence: All records are saved locally in a JSON file (weight_data.json) to maintain persistent data across sessions.
Interactive Table: View a table of your weight records, including differences from your target and estimated real gain/loss with adjusted water retention.
Decay Factor: The water retention factor decays over time based on your last input date, simulating the natural fluctuation of body water retention.
Simple Interface: A clean, intuitive user interface built with PyQt5 to make tracking weight easy and effective.




weightwise.py: The main application script that contains the PyQt5 code.
weight_data.json: The data file used to store weight and retention data. If this file does not exist, it will be created upon first run.

Weight Input: Users can input their weight using a text field.
Target Weight: Allows users to set a target weight and track progress against it.
Calendar: Choose the date for which you want to input weight data.
Weight History Table: Displays recorded weights along with the difference to target weight and real gain/loss accounting for water retention.
About Dialog: A popup that provides information about the application.
Water Retention Estimation
The app uses the following factors to estimate water retention:

Salt Intake: Low, Medium, High
Carbohydrates Intake: Low, Medium, High
Physical Activity Level: Sedentary, Moderate, Very Active
The app calculates a water retention factor based on these inputs, which influences weight gain/loss estimates.

Usage
Input Weight: Use the calendar and input field to record your weight on specific dates.
Set Target Weight: Set your desired weight target using the target weight field.
Estimate Water Retention: The application will prompt you to estimate your water retention based on your salt intake, carb consumption, and activity level.
Weight Records Table
The table displays the following columns:

Date: The date when the weight record was added.
Weight (kg): The recorded weight.
Gain/Loss to Target (kg): The difference between the recorded weight and target weight.
Real Gain/Loss (kg): The adjusted gain/loss after considering water retention.


Acknowledgements
Kipchoge the greatest runner alive!



If you enjoy this program, buy me a coffee https://buymeacoffee.com/siglabo
You can use it free of charge or build upon my code. 
 
(c) Peter De Ceuster 2024
Software Distribution Notice: https://peterdeceuster.uk/doc/code-terms 
This software is released under the FPA General Code License.
 
 

import pandas as pd

# Load data from CSV
data = pd.read_csv('asset_1.csv')

# Initialize variables
build_threshold = 0.6
liquidate_threshold = 0.2
position = 0

# Initialize the 'position' column with 0
data['position'] = 0

# Iterate through the data to update positions based on alpha values
for i in range(1, len(data)):
    previous_alpha = data.at[i-1, 'alpha']
    current_alpha = data.at[i, 'alpha']
    
    # Determine position based on thresholds and current position
    if position == 0:
        if current_alpha >= build_threshold:
            position = 1
        elif current_alpha <= -build_threshold:
            position = -1
    elif position == 1:
        if current_alpha <= liquidate_threshold:
            position = 0
    elif position == -1:
        if current_alpha >= -liquidate_threshold:
            position = 0
    
    # Record the current position
    data.at[i, 'position'] = position

# Save the updated DataFrame to a new CSV
data.to_csv('task1.csv', index=False)

# Display the first few rows of the updated DataFrame
data.head(20)

import pandas as pd

# Load the trading strategy file
data = pd.read_csv('task1.csv')

# Initialize variables
initial_position = 0
initial_price = 0
pnl = []

# Iterate through the data to calculate P&L
for i in range(1, len(data)):
    current_position = data.at[i, 'position']
    current_price = data.at[i, 'price']
    
    if current_position != initial_position:
        # Calculate the trade P&L
        if initial_position == 1:
            trade_pnl = current_price - initial_price
        elif initial_position == -1:
            trade_pnl = initial_price - current_price
        else:
            trade_pnl = 0
        
        # Record the P&L if there was an initial position
        if initial_position != 0:
            pnl.append(trade_pnl)
        
        # Update the initial position and price
        initial_position = current_position
        initial_price = current_price

# Calculate the total P&L
total_pnl = sum(pnl)

# Create a P&L DataFrame
pnl_data = {
    'Trade Number': list(range(1, len(pnl) + 1)),
    'P&L': pnl
}
pnl_df = pd.DataFrame(pnl_data)

# Add a Total P&L row
total_pnl_row = pd.DataFrame({'Trade Number': ['Total'], 'P&L': [total_pnl]})
pnl_df = pd.concat([pnl_df, total_pnl_row], ignore_index=True)

# Save the P&L statement to a new CSV file
pnl_df.to_csv('task2.csv', index=False)

# Display the P&L DataFrame
pnl_df

import pandas as pd

class TradingStrategy:
    def __init__(self, build_threshold, liquidate_threshold):
        self.build_threshold = build_threshold
        self.liquidate_threshold = liquidate_threshold
        self.position = 0
    
    def update_position(self, alpha):
        if self.position == 0:
            if alpha >= self.build_threshold:
                self.position = 1
            elif alpha <= -self.build_threshold:
                self.position = -1
        elif self.position == 1:
            if alpha <= self.liquidate_threshold:
                self.position = 0
        elif self.position == -1:
            if alpha >= -self.liquidate_threshold:
                self.position = 0
        
        return self.position

    def reset(self):
        self.position = 0
class BacktestEngine:
    def __init__(self, data):
        self.data = data
    
    def run_backtest(self, build_threshold, liquidate_threshold):
        strategy = TradingStrategy(build_threshold, liquidate_threshold)
        self.data['position'] = 0
        
        initial_position = 0
        initial_price = 0
        pnl = []
        
        for i in range(len(self.data)):
            alpha = self.data.at[i, 'alpha']
            current_price = self.data.at[i, 'price']
            current_position = strategy.update_position(alpha)
            
            if current_position != initial_position:
                if initial_position == 1:
                    trade_pnl = current_price - initial_price
                elif initial_position == -1:
                    trade_pnl = initial_price - current_price
                else:
                    trade_pnl = 0
                
                if initial_position != 0:
                    pnl.append(trade_pnl)
                
                initial_position = current_position
                initial_price = current_price
            
            self.data.at[i, 'position'] = current_position
        
        total_pnl = sum(pnl)
        return total_pnl
    
    def optimize_thresholds(self, build_thresholds, liquidate_thresholds):
        best_pnl = float('-inf')
        best_build_threshold = None
        best_liquidate_threshold = None
        
        for build_threshold in build_thresholds:
            for liquidate_threshold in liquidate_thresholds:
                pnl = self.run_backtest(build_threshold, liquidate_threshold)
                if pnl > best_pnl:
                    best_pnl = pnl
                    best_build_threshold = build_threshold
                    best_liquidate_threshold = liquidate_threshold
        
        return best_build_threshold, best_liquidate_threshold, best_pnl
# Load the data
data = pd.read_csv('asset_1.csv')

# Define the range for thresholds
build_thresholds = [x / 10.0 for x in range(1, 10)]
liquidate_thresholds = [x / 10.0 for x in range(1, 10)]

# Initialize the backtest engine
engine = BacktestEngine(data)

# Find the optimal thresholds
best_build_threshold, best_liquidate_threshold, best_pnl = engine.optimize_thresholds(build_thresholds, liquidate_thresholds)

print(f"Optimal Build Threshold: {best_build_threshold}")
print(f"Optimal Liquidate Threshold: {best_liquidate_threshold}")
print(f"Maximized P&L: {best_pnl}")

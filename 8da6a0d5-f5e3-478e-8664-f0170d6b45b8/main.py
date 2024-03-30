from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Define the ticker symbol for the asset we're interested in.
        self.ticker = "TQQQ"

    @property
    def assets(self):
        # The strategy will only focus on TQQQ.
        return [self.ticker]

    @property
    def interval(self):
        # Use daily intervals for SMA calculation.
        return "1day"

    def run(self, data):
        # Calculate short-term and long-term SMAs for TQQQ.
        short_term_sma = SMA(self.ticker, data["ohlcv"], length=20)  # 20-day SMA
        long_term_sma = SMA(self.ticker, data["ohlcv"], length=50)  # 50-day SMA

        # Initialize the allocation with no investment.
        allocation = {self.ticker: 0}

        # Ensure we have enough data points for both SMAs to make a decision.
        if len(short_term_sma) >= 50 and len(long_term_sma) >= 50:
            # If the short-term SMA crosses above the long-term SMA, it's a buy signal.
            if short_term_sma[-1] > long_term_sma[-1] and short_term_sma[-2] <= long_term_sma[-2]:
                log("Buy signal detected.")
                allocation[self.ticker] = 1  # Allocate 100% of the portfolio to TQQQ.
            # If the short-term SMA crosses below the long-term SMA, it's a sell signal.
            elif short_term_sma[-1] < long_term_sma[-1] and short_term_sma[-2] >= long_term_sma[-2]:
                log("Sell signal detected.")
                allocation[self.ticker] = 0  # Hold no TQQQ.
        
        # Return the target allocation as a TargetAllocation object.
        return TargetAllocation(allocation)
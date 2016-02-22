#!/usr/bin/env python
import sys
import mutetoolbox.strategies

data = [1, 34, 5, 6, 12]

print("Classic OO")
binning = mutetoolbox.strategies.BinningStrategy()
binning.set_data(data)
binning.run()
print(binning.get_results())

average = mutetoolbox.strategies.AverageStrategy()
average.set_data(data)
average.run()
print(average.get_results())

print("Fancy OO")
strategies = [mutetoolbox.strategies.BinningStrategy(), mutetoolbox.strategies.AverageStrategy()]
for strategy in strategies:
    strategy.set_data(data)
    strategy.run()
    sys.stdout.write(strategy.get_strategy_name() + " results: ")
    print(strategy.get_results())

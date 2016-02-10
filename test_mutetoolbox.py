#!/usr/bin/env python
import mutetoolbox.strategies

print("Classc OO")
data = [1,34,5,6,12]
binning = mutetoolbox.strategies.BinningStrategy()
binning.setData(data)
binning.run()

average =  mutetoolbox.strategies.AverageStrategy()
average.setData(data)
average.run()

print("Fancy OO")
strategies = []
strategies.append(mutetoolbox.strategies.BinningStrategy())
strategies.append(mutetoolbox.strategies.AverageStrategy())
for strategy in strategies:
	strategy.setData(data)
	strategy.run()


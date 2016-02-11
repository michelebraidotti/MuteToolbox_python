#!/usr/bin/env python
import sys
import mutetoolbox.strategies

data = [1,34,5,6,12]



print("Classc OO")
binning = mutetoolbox.strategies.BinningStrategy()
binning.setData(data)
binning.run()
print binning.getResults()

average =  mutetoolbox.strategies.AverageStrategy()
average.setData(data)
average.run()
print average.getResults()



print("Fancy OO")
strategies = []
strategies.append(mutetoolbox.strategies.BinningStrategy())
strategies.append(mutetoolbox.strategies.AverageStrategy())
for strategy in strategies:
	strategy.setData(data)
	strategy.run()
	sys.stdout.write( strategy.getStrategyName() + " results: " )
	print strategy.getResults()


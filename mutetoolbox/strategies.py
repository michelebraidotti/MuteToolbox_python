class AbstractStrategy():
	def __init__(self):
		self.results = ""
	def setData(self, data):
		self.data = data
	def getResults(self):
		return self.results
	def getStrategyName(self):
		raise NotImplementedError('Abstract method should not be used directly')
	def run(self):
		raise NotImplementedError('Abstract method should not be used directly')

class BinningStrategy(AbstractStrategy):
	def run(self):
		binBig = []
		binSmall = []
		for d in self.data:
			if ( d > 10 ):
				binBig.append(d)
			else:
				binSmall.append(d)
		self.results = "Small bin has %i elems, Big bin as %i elems" % ( len(binSmall) , len(binBig) ) 
	def getStrategyName(self):
		return 'Binning'

class AverageStrategy(AbstractStrategy):
	def run(self):
		sum = 0
		for d in self.data:
			sum += d
		self.results = "Average is %i" % ( sum/len(self.data) )
	def getStrategyName(self):
		return 'Average'


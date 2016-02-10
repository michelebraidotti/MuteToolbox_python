class AbstractStrategy():
	def setData(self, data):
		self.data = data
	def run(self):
		# abstract method!
		raise NotImplementedError('abstract method should not be used directly')

class BinningStrategy(AbstractStrategy):
	def run(self):
		binBig = []
		binSmall = []
		for d in self.data:
			if ( d > 10 ):
				binBig.append(d)
			else:
				binSmall.append(d)
		print("Small bin has",len(binSmall),"elems, Big bin as",len(binBig),"elems\n")

class AverageStrategy(AbstractStrategy):
	def run(self):
		sum = 0
		for d in self.data:
			sum += d
		print("Average is",sum/len(self.data))

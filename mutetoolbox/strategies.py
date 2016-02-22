class AbstractStrategy:
    def __init__(self):
        self.results = ""
        self.data = []

    def set_data(self, data):
        self.data = data

    def get_results(self):
        return self.results

    def get_strategy_name(self):
        raise NotImplementedError('Abstract method should not be used directly')

    def run(self):
        raise NotImplementedError('Abstract method should not be used directly')


class BinningStrategy(AbstractStrategy):
    def run(self):
        bin_big = []
        bin_small = []
        for d in self.data:
            if d > 10:
                bin_big.append(d)
            else:
                bin_small.append(d)
        self.results = "Small bin has %i elements, Big bin as %i elements" % (len(bin_small), len(bin_big))

    def get_strategy_name(self):
        return 'Binning'


class AverageStrategy(AbstractStrategy):
    def run(self):
        sum_data = 0
        for d in self.data:
            sum_data += d
        self.results = "Average is %i" % (sum_data / len(self.data))

    def get_strategy_name(self):
        return 'Average'

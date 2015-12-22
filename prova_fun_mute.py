import numpy as np
from utils import *
from class_System import *
import scipy.io

data = scipy.io.loadmat('/Users/alessandromontalto/Dropbox/MuTE_pythonVersion/realization5000p_1.mat')
# data = np.array([[1, 8, 3, 1, 6, 7, 8, 1, 5, 8, 9, 1, 3, 5, 6 ,3], [4, 0, 2, 4, 5, 2, 0, 4, 0, 3, 1, 2, 3, 1, 0, 5], [2, 3, 4, -3, 1, 1, 3, 2, 3, 3 , 4, 5, 5, 4, 7, -8]])#np.array([[1,2,3,4,5,6,7,8,9,10], [11,12,13,14,15,16,17,18,19,20], [31,32,33,34,35,36,37,38,39,40]])#np.random.randn(3, 10)
# print(type(data['data']))
# e = binEntropy(data)
# print(e)
s =  complexSystem(data['data'][:][1:600])
s.params['series4analysis'] = []#['series0', 'series4', 'series6', 'series9', 'series3']
s.params['delays'] = np.array([5, 1, 1]) #np.array([[4, 3, 2], [3, 1, 1], [4, 2, 1], [3, 2, 5], [1, 3, 5]])
s.params['mode'] = 'biv'
s.params['combinations'] = 'allPairWise'
s.params['listTDC'] = [[['series0'],['series1']],[['series1'],['series0']]]#[[['series7'], ['series4']], [['series4'], ['series6', 'series9'], ['series7']], [['series6'], ['series6'], ['series9', 'series4']]]
s.params['quantization'] = {'numberOfBins' : 5}
s.params['surrogates'] = {'howMany' : 150, 'alphaPercentile' : 0.05, 'how2shuffle' : 'randomPermutation'}
# th, boh = surrogatesTest(s, data, 0.04)
# print(th, boh)
s.binnue()

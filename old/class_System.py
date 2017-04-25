from utils import *
import copy
import sys

class complexSystem:

	import numpy as np

	def __init__(self, data, selectedTimeSeries):
		# print(data)
		#data has to be a matrix of numSubSystems x numTimePoints dimensions
		if not data.size:
			sys.exit('MuTE Error: "data" must not be empty')
		self.data = data
		self.selectedTimeSeries = selectedTimeSeries #selectedTimeSeries is a vector that stores the time series that you actually want to use in your analysis. Ex. you have a 12x200 data matrix. You might only want to analyse a subset of the 12 variables.
		self.candidates = {}
		self.systemDict = {}
		self.dictAnalyses = {}
		self.params = {}

	def buildSystemDict(self):
		if not self.data.size:
			sys.exit('MuTE Error: initialization step required. Please initialize your "System" object' + 
				' providing data')
		systemDict = {}
		for idSubS in range(self.data.shape[0]):
			systemDict['series' + str(idSubS)] = self.data[idSubS][:]
		self.systemDict = systemDict

	def isSeriesPresent(self, nameSeries, dictionary):
		maxIdSeries = 0
		for series in nameSeries:
			if series not in dictionary:
				return False
		return True

	def buildCandidates(self):
		delays = copy.copy(self.params['delays'])
		nameSeries = copy.copy(self.params['series4analysis'])
		if delays.ndim == 1:
			numDelayedSubS = 1
		else:
			numDelayedSubS = delays.shape[0]
		if numDelayedSubS == 1 and nameSeries == []:
			print('***** The user decided to consider all the time series *****')
			print('The same candidates will be chosen for every time series')
			for idSubS in range(self.data.shape[0]):
				self.candidates['series' + str(idSubS)] = getDelay(delays, idSubS)
		elif numDelayedSubS == 0:
			sys.exit('MuTE Error: The variable delays must not be empty')
		else:
			if numDelayedSubS == 1 and len(nameSeries) > 1:
				if not self.isSeriesPresent(nameSeries, self.systemDict):
					sys.exit('MuTE Error: One or more series in "series4analysis" do not belong to "self.systemDict"')
				print('The same candidates will be chosen for the selected time series: from now on ' +
					'the analysis must take into account the selected series only')
				for idSubS in range(len(nameSeries)):
					self.candidates['series' + nameSeries[idSubS][6:]] = getDelay(delays, idSubS)
			elif nameSeries == []:
				sys.exit('MuTE Error: If "delays" is a matrix "series4analysis" cannot be empty')
			else:
				if numDelayedSubS != len(nameSeries):
					sys.exit('MuTE Error: number of "delays" rows and number of selected time series must match')
					return
				series2delay = len(nameSeries)
				if series2delay == 1:
					if not self.isSeriesPresent(nameSeries, self.systemDict):
						sys.exit('MuTE Error: One or more series in "series4analysis" do not belong to "self.systemDict"')
					print('Only the selected time series will have candidates: from now on ' +
					'the analysis must take into account the selected series only')
					for series in range(series2delay):
						self.candidates[nameSeries[series]] = getDelay(delays, idSubS)
				else:
					if not self.isSeriesPresent(nameSeries, self.systemDict):
						sys.exit('MuTE Error: One or more series in "series4analysis" do not belong to "self.systemDict"')
					print('Candidates will be attached to the selected time series: from now on \n' +
					'the analysis must take into account the selected series only')
					for series in range(series2delay):
						self.candidates[nameSeries[series]] = getDelay(delays[series][:], nameSeries[series][-1:])

	def getAllPairWiseComb(self):
		mode = copy.copy(self.params['mode'])
		nameSeries = copy.copy(self.params['series4analysis'])
		if not nameSeries:
			nameSeries = self.candidates.keys()
		numSeries = len(nameSeries)
		dictAnalyses = {}
		numCurrDict  = 0
		if mode == 'biv':
			print('Arranging all target-drivers combinations')
			for i in range(numSeries):
				if i == 0:
					for j in range(1, numSeries):
						dictAnalyses['analysis' + str(numCurrDict)] = buildDict_TDC([['series' + nameSeries[i][6:]], ['series' + nameSeries[j][6:]]])
						numCurrDict += 1
				else:
					idSeries = range(0,i) + range(i+1,numSeries)
					for j in idSeries:
						dictAnalyses['analysis' + str(numCurrDict)] = buildDict_TDC([['series' + nameSeries[i][6:]], ['series' + nameSeries[j][6:]]])
						numCurrDict += 1
		elif mode == 'multiv':
			print('Arranging all target-drivers-conditioning combinations')
			numAvailableSeries = range(numSeries)
			idCondSeries = []
			for i in range(numSeries):
				if i == 0:
					for j in range(1, numSeries):
						nameCondSeries = [''] * (numSeries - 2)
						tmpNumAvailableSeries = copy.copy(numAvailableSeries)
						tmpNumAvailableSeries.remove(i)
						tmpNumAvailableSeries.remove(j)
						k = 0
						for idCondSeries in tmpNumAvailableSeries:
							nameCondSeries[k] = 'series' + nameSeries[idCondSeries][6:]
							k += 1
						dictAnalyses['analysis' + str(numCurrDict)] = buildDict_TDC([['series' + nameSeries[i][6:]], ['series' + nameSeries[j][6:]], nameCondSeries])
						numCurrDict += 1
				else:
					idSeries = range(0,i) + range(i+1,numSeries)
					for j in idSeries:
						nameCondSeries = [''] * (numSeries - 2)
						tmpNumAvailableSeries = copy.copy(numAvailableSeries)
						tmpNumAvailableSeries.remove(i)
						tmpNumAvailableSeries.remove(j)
						k = 0
						for idCondSeries in tmpNumAvailableSeries:
							nameCondSeries[k] = 'series' + nameSeries[idCondSeries][6:]
							k += 1
						dictAnalyses['analysis' + str(numCurrDict)] = buildDict_TDC([['series' + nameSeries[i][6:]], ['series' + nameSeries[j][6:]], nameCondSeries])
						numCurrDict += 1
		else:
			sys.exit('MuTE Error: "mode" name must be either "biv" or "multiv"')
		self.dictAnalyses = dictAnalyses

	def setAnalysis(self):
		if 'mode' not in self.params:
			sys.exit('MuTE Error: "mode" parameter must be provided')
		if 'combinations' not in self.params:
			sys.exit('MuTE Error: "combinations" parameter must be provided')
		if 'listTDC' not in self.params:
			sys.exit('MuTE Error: "listTDC" parameter must be provided')
		mode = copy.copy(self.params['mode'])
		combinations = copy.copy(self.params['combinations'])
		# nameSeries = copy.copy(self.params['series4analysis'])
		listTDC = copy.copy(self.params['listTDC'])
		if combinations == 'allPairWise':
			print('***** "listTDC" will not be taken into account *****')
			self.getAllPairWiseComb()
		elif combinations == 'manual':
			dictAnalyses = {}
			for i in range(len(listTDC)):
				for j in range(len(listTDC[i])):
					if not self.isSeriesPresent(listTDC[i][j], self.candidates):
						sys.exit('MuTE Error: One or more series in "listTDC" do not belong to "self.candidates" \n')
			if listTDC:
				print('Arranging all target-drivers-conditioning combinations as set by the user')
				for i in range(len(listTDC)):
					dictAnalyses['analysis' + str(i)] = buildDict_TDC(listTDC[i])
				self.dictAnalyses = dictAnalyses
			else:
				sys.exit('MuTE Error: listTDC can not be empty if "manual" mode is chosen')
		else:
			sys.exit('MuTE Error: "combinations" can only assume either "allPairWise" or "manual" values')



	def binnue(self):
		#I think that it would be better to create a statisticalApproaches that inherit complexSistem. What I would like to have is something like
		#binnue.method() where binnue has its own parameters. Can this scenario be achieved even with this structure?
		if not (self.params):
			sys.exit('MuTE Error: initialization step required. Please initialize your "System" object' + 
				' filling "params" dictionary')
		# building all attributes according to "params" fields
		self.buildSystemDict()
		self.buildCandidates()
		self.setAnalysis()
		if 'quantization' in self.params:
			print('Quantization preprocessing occurring')
			quantizedData = quantization(self)
			self.systemDict = quantizedData
		print('***** Starting evaluating the second entropy term: the drivers are taken into account *****')
		secondTermCE, finalCandidates, CMI, minCEList = eval_2TermCE(self)
		# print(secondTermCE, finalCandidates, CMI, minCEList)
		print('***** Starting evaluating the first entropy term: the drivers are not taken into account *****')
		firstTermCE = eval_1TermCE(self, finalCandidates)


























from __future__ import division
import numpy as np
import copy
import random
import sys

def getDelay(delays, idSubS):
	#delays[0] = model order
	#delays[1] = lag
	#delays[2] = delay
	mtxDelays = np.zeros((delays[0],2))
	for i in range(delays[0]):
		mtxDelays[i][0] = idSubS
		mtxDelays[i][1] = delays[2] + (i * delays[1])
	return mtxDelays

def buildDict_TDC(TDC_list):
	dictTDC = {}
	dictTDC['targets'] = TDC_list[0]
	dictTDC['drivers'] = TDC_list[1]
	if len(TDC_list) == 3:
		dictTDC['conditioning'] = TDC_list[2]
	return dictTDC

def quantization(self):
	quantizedData = {}
	numQuantumLevels = self.params['quantization']['numberOfBins']
	numSeries = len(self.candidates.keys())
	amplitudeLevel = [0] * numSeries
	valueMin = [0] * numSeries
	valueMax = [0] * numSeries
	quantumLevels = np.zeros((numQuantumLevels, numSeries))
	i = 0
	for series in self.candidates.keys():
		valueMin[i] = min(self.systemDict[series])
		valueMax[i] = max(self.systemDict[series])
		amplitudeLevel[i] += (valueMax[i] - valueMin[i]) / numQuantumLevels
		i += 1
	for j in range(self.params['quantization']['numberOfBins']):
		for i in range(numSeries):
			quantumLevels[j][i] = valueMin[i] + (amplitudeLevel[i] * (j+1))
	i = 0
	for series in self.candidates.keys():
		tmpQuantData = self.systemDict[series]
		for j in range(len(self.systemDict[series])):
			idLevels = 0 
			while  (idLevels < numQuantumLevels) and (self.systemDict[series][j] >= quantumLevels[idLevels][i]):
					idLevels += 1
					if idLevels == numQuantumLevels:
						break
			tmpQuantData[j] = idLevels
		quantizedData[series] = tmpQuantData
		i += 1
	return quantizedData

def pickMaxDelay(delayList):
	maxDelay = [0, 0]
	for element in delayList:
		if element[1] > maxDelay[1]:
			maxDelay = copy.copy(element)
	return maxDelay

def mergeCandidates(self, analysis):
	targets = self.dictAnalyses[analysis]['targets'][0]
	drivers = self.dictAnalyses[analysis]['drivers']
	candidates = self.candidates[targets]
	for series in drivers:
		candidates = np.concatenate([candidates, self.candidates[series]])
	if 'conditioning' in self.dictAnalyses[analysis]:
		conditioning = self.dictAnalyses[analysis]['conditioning']
		for series in conditioning:
			candidates = np.concatenate([candidates, self.candidates[series]])
	return candidates

def buildMatrixDelay(self, candidates = None, nameAnalysis = None):
	sysDict = copy.copy(self.systemDict)
	timePoints = len(self.data[0])
	if candidates is not None:
		maxDelay = pickMaxDelay(candidates)
		numSeries = len(candidates)
		mtxDelay = np.zeros((numSeries, timePoints-maxDelay[1]))
		matrixDelay = {}
		series = 0
		for element in candidates:
			if element[1] == 0:
				mtxDelay[series] = copy.copy(self.systemDict['series' + str(int(element[0]))][maxDelay[1] :])
			else:
				e = str(element[0])
				mtxDelay[series] = copy.copy(self.systemDict['series' + e[0]][maxDelay[1]-element[1] : -element[1]])
			series += 1
		if nameAnalysis is not None:
			matrixDelay[nameAnalysis] = mtxDelay
		else:
			matrixDelay['analysis0'] = mtxDelay
	else:
		matrixDelay = {}
		for analysis in self.dictAnalyses:
			candidates = mergeCandidates(self, analysis)
			maxDelay = pickMaxDelay(candidates)
			numSeries = len(candidates)
			mtxDelay = np.zeros((numSeries, timePoints-maxDelay[1]))
			series = 0
			for element in candidates:
				if element[1] == 0:
					mtxDelay[series] = copy.copy(self.systemDict['series' + str(element[0])][maxDelay[1] :])
				else:
					e = str(element[0])
					mtxDelay[series] = copy.copy(self.systemDict['series' + e[0]][maxDelay[1]-element[1] : -element[1]])
				series += 1
			matrixDelay[analysis] = mtxDelay
	return matrixDelay

def countOccurrences(matrix, vector):
	if vector.shape[0] == 1:
		vector = vector.transpose()
	idOccurrences = np.argwhere(np.all(matrix-vector==0, axis=0))
	numOccurrences = len(idOccurrences)
	mtx_wout_vector = np.delete(matrix,idOccurrences,1)
	return numOccurrences, idOccurrences, mtx_wout_vector

def binEntropy(matrix):
	totConfig = matrix.shape[1]
	config = copy.copy(matrix)
	entropy = 0
	f = 0
	while config.size:
		numOccurrences, idOccurrences, config = countOccurrences(config, np.array([config[:,0]]))
		entropy = entropy - ((numOccurrences/totConfig) * np.log(numOccurrences/totConfig))
	return entropy

def conditionalEntropy(matrix):
	matrixWithoutTarget = matrix[1:][:]
	CE_full = binEntropy(matrix)
	CE_reduced = binEntropy(matrixWithoutTarget)
	return CE_full - CE_reduced, CE_full, CE_reduced

def surrogatesTest(self, matrix, realE):
	numSurrogates = self.params['surrogates']['howMany']
	alphaPercentile = self.params['surrogates']['alphaPercentile']
	shuffleMode = self.params['surrogates']['how2shuffle']
	surrogatesMatrix = []
	CE = []
	matrixDim = matrix.shape
	for s in range(numSurrogates):
		if shuffleMode == 'randomPermutation':
			shuffledCandidate = copy.copy(matrix[-1])
			np.random.shuffle(shuffledCandidate)
			surrogatesMatrix.append(shuffledCandidate)
	if matrixDim[0] > 2:
		mtxNoTarget = matrix[1:-2][:]
		mtxWithTarget = matrix[0:-2][:]
	else:
		mtxNoTarget = np.array([])
		mtxWithTarget = matrix[0][:]
	surrogatesMatrix = np.array(surrogatesMatrix)
	for s in range(numSurrogates):
		if matrixDim[0] > 2:
			mtxE_full = np.concatenate([np.array([mtxWithTarget]), np.array([surrogatesMatrix[s][:]])])
			mtxE_reduced = np.concatenate([np.array([mtxNoTarget]), np.array([surrogatesMatrix[s][:]])])
		else:
			mtxE_full = np.concatenate([np.array([mtxWithTarget]), np.array([surrogatesMatrix[s][:]])])
			mtxE_reduced = np.array([surrogatesMatrix[s][:]])
		CE.append(binEntropy(mtxE_full) - binEntropy(mtxE_reduced))
	CE_noRealE = [element - realE for element in CE]
	threshold = np.percentile(CE_noRealE, 100 * (1 - alphaPercentile))
	return threshold, surrogatesMatrix

def eval_2TermCE(self):
	minCEList = {}
	CMI = {}
	finalCandidates = {}
	finalCE = {}
	threshold = {}
	for analysis in self.dictAnalyses:
		shannonEntropy = binEntropy(np.array([self.systemDict[self.dictAnalyses[analysis]['targets'][0]]]))
		candidates = mergeCandidates(self, analysis)
		originalCandSize = candidates.size
		minCEList[analysis] = [['shanonE', shannonEntropy]]
		# Conditional Mutual Information = CMI
		CMI[analysis] = []
		finalCandidates[analysis] = np.array([])
		finalCE[analysis] = []
		threshold[analysis] = []
		th = []
		# while candidates.size:
		for can in candidates:
			print('can = ',can, 'analysis = ', analysis)
			copy_candidates = copy.copy(candidates)
			CE = {}
			c = 0
			for candidate in copy_candidates:
				print(type(candidate), type(finalCandidates[analysis]))
				if candidate not in finalCandidates[analysis]:
					candArrayVersion = np.array([candidate])
					if not finalCandidates[analysis].size: # It is the first iteration of the loop
						# Adding the present of the target at the top of the candidate list
						targetArray = np.array([[int(self.dictAnalyses[analysis]['targets'][0][6:]), 0]])
						tmpCand = np.concatenate((targetArray, candArrayVersion))
						# Building tha matrix of delays taking into account the candidate list that contains the present of the target
						matrixDelay = buildMatrixDelay(self, tmpCand)['analysis0']
					else: # The body of the else is executed after the first candidate is chosen
						# finalCandidatesArrayVersion = np.array([finalCandidates[analysis]])
						print('controlliamo se entra qui', targetArray.shape, finalCandidates[analysis].shape, candArrayVersion.shape)
						# sys.exit()
						matrixDelay = buildMatrixDelay(self, np.concatenate((targetArray, finalCandidates[analysis], candArrayVersion)))['analysis0']
					# tmpCE[str(c)], CE_full, CE_reduced = conditionalEntropy(matrixDelay)
					# CE[analysis] = copy.copy(tmpCE)
					CE[str(c)], CE_full, CE_reduced = conditionalEntropy(matrixDelay)
					c += 1
			for key in CE.keys():
				if CE[key] < minCEList[analysis][0][1]:
					minKey = key
					minCE = CE[key]
					minCEList[analysis].append([minKey, minCE])
			CMI[analysis].append(minCEList[analysis][-2][1] - minCEList[analysis][-1][1])
			print(minCEList[analysis][-2][1] - minCEList[analysis][-1][1], CMI[analysis])
			# Statistical test to assess whether the candidate is significant
			tmpTh, surroMtx = surrogatesTest(self, matrixDelay, minCEList[analysis][-1][1])
			th.append(tmpTh)
			print('th = ', th, CMI[analysis], can.all() == candidates[0].all())
			if CMI[analysis][-1] > th[-1]:
				print('finalCandidates = ', finalCandidates[analysis])
				finalCandidates[analysis] = np.row_stack([copy_candidates[(int(minCEList[analysis][-1][0]))][:]])# .append([copy_candidates[(int(minCEList[analysis][-1][0]))][:]])
				print('finalCandidates = ', finalCandidates[analysis])
				# copy_candidates = np.delete(copy_candidates, (int(minCEList[analysis][-1][0])), axis = 0)
			elif CMI[analysis][-1] <= th[-1] and can.all() == candidates[0].all():
				print('MuTE Warning: according to this method there are no significant candidates')
				break
			else:
				# copy_candidates = []
				break
		finalCE[analysis].append(minCEList[analysis][-1][1])
		threshold[analysis].append(th)
	return finalCE, finalCandidates, CMI, minCEList

def eval_1TermCE(self, finalCandidates):
	candidates_1TermCE = {}
	CE_1Term = {}
	for analysis in finalCandidates.keys():
		candidates_1TermCE[analysis] = copy.copy(finalCandidates[analysis])
		for driver in self.dictAnalyses[analysis]['drivers']:
			if driver in finalCandidates[analysis]:
				print(driver, finalCandidates)
				candidates_1TermCE[analysis].remove(driver)
		targetArray = np.array([[int(self.dictAnalyses[analysis]['targets'][0][6:]), 0]])
		candidates_1TermCE_ArrayVersion = np.array([candidates_1TermCE[analysis]])
		# print(targetArray, candidates_1TermCE_ArrayVersion)
		matrixDelay = buildMatrixDelay(self, np.concatenate((targetArray, candidates_1TermCE_ArrayVersion)))['analysis0']
		CE_1Term[analysis], CE_full, CE_reduced = conditionalEntropy(matrixDelay)
	return CE_1Term



































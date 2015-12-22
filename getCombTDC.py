def buildDict_TDC(TDC_list):
	dictTDC = {}
	dictTDC{'targets'} = TDC_list[0]
	dictTDC{'drivers'} = TDC_list[1]
	dictTDC{'conditioning'} = TDC_list[2]
	return dictTDC




def getCombTDC(candidates, mode, combinations, nameTarSeries = '', nameDrivSeries = '', nameCondSeries = ''):
	if mode == 'biv':
		# take into account nameTarSeries and nameDrivSeries only
		# return a matrix of strings with the series names according to combinations
		if combinations == 'allPairWise':
			# return all the pairwise combinations or target-drivers
			numSeries = len(candidates.keys())
			analysis = np.chararray((2, numSeries*(numSeries-1)))
			for i in range(numSeries):
				analysis[0][numSeries*i : numSeries*(i+1)-1] = 'series' + str(i)
				if i == 0:
					seriesArray = np.chararray()
					for j in range(numSeries-1):
						seriesArray[j] = 'series' + str(j+1)
					analysis[1][numSeries*i : numSeries*(i+1)-1] = seriesArray
				else:
					seriesArray = np.chararray()
					idSeries = [range(0,i) range(i+1,numSeries)]
					for j in idSeries:
						seriesArray[j] = 'series' + str(j)
					analysis[1][numSeries*i : numSeries*(i+1)-1] = seriesArray
		else:
			# *************    FUNCTION TO BE IMPLEMENTED   *************
			#
			# check whether targets, drivers, conditioning variables are among the variables in the candidates dictionary
			#
			# *************    FUNCTION TO BE IMPLEMENTED   *************
			
	elif mode == 'multiv':
		if combinations == 'allPairWise':
			# return all the pairwise combinations or target-drivers, conditioned to all the other variables choosen
			numSeries = len(candidates.keys())
			analysis = np.chararray((2+(numSeries-2), numSeries*(numSeries-1)))
			
		else:
	else
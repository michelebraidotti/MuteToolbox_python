import numpy as np

def getDelay(delays):
	#delays[0] = model order
	#delays[1] = lag
	#delays[2] = delay
	mtxDelays = np.zeros((delays[0],1))
	for i in range(delays[0]):
		mtxDelays[i] = delays[2] + (i * delays[1])
	#print(mtxDelays)
	return mtxDelays
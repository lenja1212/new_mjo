import numpy as np
import pandas as pd
from pathlib import Path

def findCor(pc1_all_memb, pc2_all_memb, memb_to_draw): ### W:  
	print("findCor")
	corr = []
	pc_days = len(pc1_all_memb[0])
	for i in range(0, pc_days):
		dayly_pc1, dayly_pc2 = getDaylyPc(pc1_all_memb, pc2_all_memb, memb_to_draw, i)
		numenator_pc1 = pc1_all_memb[-1][i] * np.sum(dayly_pc1) #a1 * b1
		numenator_pc2 = pc2_all_memb[-1][i] * np.sum(dayly_pc2) #a2 * b2
		denom_1 = np.sqrt( memb_to_draw * np.power(pc1_all_memb[-1][i], 2)  + memb_to_draw * np.power(pc2_all_memb[-1][i], 2) )  
		denom_2 = np.sqrt( np.sum(np.power(dayly_pc1, 2)) + np.sum(np.power(dayly_pc2, 2)) )
		corr.append( (numenator_pc1 + numenator_pc2) / (denom_1 * denom_2) )

	return corr

def findRmse(pc1_all_memb, pc2_all_memb, memb_to_draw): #
	print("findRmse")
	rmse = []
	pc_days = len(pc1_all_memb[0])
	for i in range(0, pc_days): 
		dayly_pc1, dayly_pc2 = getDaylyPc(pc1_all_memb, pc2_all_memb, memb_to_draw, i)
		delta_1 = pc1_all_memb[-1][i] - np.array(dayly_pc1)
		delta_2 = pc2_all_memb[-1][i] - np.array(dayly_pc2)
		numenator_1 = np.sum( np.power(delta_1, 2 ) ) 
		numenator_2 = np.sum( np.power(delta_2, 2 ) ) 
		rmse.append( np.sqrt( (numenator_1 + numenator_2) / memb_to_draw) )
		print("rmse[",i,"]: ",rmse[i])
	print()
	return rmse

def findMsss(pc1_all_memb, pc2_all_memb, memb_to_draw):
	print("findMsss")
	msss = []
	mse_c = []
	pc_days = len(pc1_all_memb[0])
	rmse = findRmse(pc1_all_memb, pc2_all_memb, memb_to_draw)
	mse_f = np.power(rmse, 2)
	for i in range(0, pc_days): # days in pc
		mse_c_numen = memb_to_draw * ( np.power(pc1_all_memb[-1][i], 2)  + np.power(pc2_all_memb[-1][i], 2) )
		mse_c.append(mse_c_numen / memb_to_draw) 
	print("mse_f: ", mse_f)
	print("mse_c: ", mse_c)
	print("mse_f/mse_: ", mse_f/mse_c)

	msss = 1 - mse_f / mse_c
	for i in range(0, pc_days): # days in pc
		print("msss[",i,"]: ",msss[i])
	# exit()
	return msss

def getMaxMinMedMemb(pc1_all_memb, pc2_all_memb, memb_to_draw): #!!!
	elements_pc1_max = []
	elements_pc1_min = []
	elements_pc2_max = []
	elements_pc2_min = []
	pc1_mean_arr = []
	pc2_mean_arr = []
	for i in range(0, len(pc1_all_memb[0])): #days to draw
		pc1_mean = 0 
		pc2_mean = 0
		dayly_pc1, dayly_pc2 = getDaylyPc(pc1_all_memb, pc2_all_memb, memb_to_draw, i)

		pc1_mean_arr.append(np.median(dayly_pc1))
		pc2_mean_arr.append(np.median(dayly_pc2))

		elements_pc1_max.append(np.percentile(dayly_pc1, 75))
		elements_pc1_min.append(np.percentile(dayly_pc1, 25))
		elements_pc2_max.append(np.percentile(dayly_pc2, 75))
		elements_pc2_min.append(np.percentile(dayly_pc2, 25))

	return elements_pc1_max, elements_pc2_max, elements_pc1_min, elements_pc2_min, pc1_mean_arr, pc2_mean_arr


def getDaylyPc(pc1_all_memb, pc2_all_memb, memb_to_draw, day):
	dayly_pc1 = []
	dayly_pc2 = []
	for j in range(0, memb_to_draw): # i-th day in all months  #len(pc1_all_memb)
		dayly_pc1.append(pc1_all_memb[j][day])
		dayly_pc2.append(pc2_all_memb[j][day])
	return dayly_pc1, dayly_pc2



	# for i in range(0, pc_days):
	# 	dayly_pc1, dayly_pc2 = getDaylyPc(pc1_all_memb, pc2_all_memb, memb_to_draw, i)
	# 	print("dayly_pc1: ", dayly_pc1)
	# 	print("dayly_pc2: ", dayly_pc2)
	# 	print("pc1_all_memb[-1][i]: ", pc1_all_memb[-1][i])
	# 	print("pc2_all_memb[-1][i]: ", pc2_all_memb[-1][i])
	# 	print("np.sum(dayly_pc1): ", np.sum(dayly_pc1))
	# 	print("np.sum(dayly_pc2): ", np.sum(dayly_pc2))
	# 	numenator_pc1 = pc1_all_memb[-1][i] * np.sum(dayly_pc1) #a1 * b1
	# 	numenator_pc2 = pc2_all_memb[-1][i] * np.sum(dayly_pc2) #a2 * b2
	# 	print("numenator_pc1: ",numenator_pc1)
	# 	print("numenator_pc2: ",numenator_pc2)
	# 	print()
	# 	print("np.power(pc1_all_memb[-1][i], 2): ", np.power(pc1_all_memb[-1][i], 2))
	# 	print("np.power(pc2_all_memb[-1][i], 2): ", np.power(pc2_all_memb[-1][i], 2))
	# 	denom_1 = np.sqrt( memb_to_draw * np.power(pc1_all_memb[-1][i], 2)  + memb_to_draw * np.power(pc2_all_memb[-1][i], 2) )  
	# 	denom_2 = np.sqrt( np.sum(np.power(dayly_pc1, 2)) + np.sum(np.power(dayly_pc2, 2)) )
	# 	print("denom_1: ",denom_1)
	# 	print("denom_2: ",denom_2)
	# 	print("numenator: ", (numenator_pc1 + numenator_pc2) )
	# 	print("denom: ", (denom_1 * denom_2))
	# 	corr.append( (numenator_pc1 + numenator_pc2) / (denom_1 * denom_2) )
	# 	print("corr[",i,"]: ",corr[i])
	# 	print()
	# 	print()
	# return corr
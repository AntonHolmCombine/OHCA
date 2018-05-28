import glob
import os
from shutil import copyfile

trees = glob.glob(os.getcwd()+"\\tree_*")
nbrOfTrees = len(trees)
allTerminal = False
terminals = []
stepTracker = 0

while(not(allTerminal)):
	os.mkdir(os.getcwd() + "\\step_" + str(stepTracker))
	for currTree in trees:
		if(currTree in terminals):
			currLen = len(glob.glob(currTree+"\\*.png"))
			copyfile(currTree+"\\patient_depth_"+str(currLen-1)+".png",
				os.getcwd()+"\\step_"+str(stepTracker)+"\\tree_"+str(currTree.split("tree_")[1])+"_step_"+str(stepTracker)+".png")
		else:
			copyfile(currTree+"\\patient_depth_"+str(stepTracker)+".png",
				os.getcwd()+"\\step_"+str(stepTracker)+"\\tree_"+str(currTree.split("tree_")[1])+"_step_"+str(stepTracker)+".png")
			currLen = len(glob.glob(currTree+"\\*.png"))
			if(currLen-1<=stepTracker):
				terminals.append(currTree)
	
	if(len(terminals)>=nbrOfTrees):
		allTerminal = True
	stepTracker += 1
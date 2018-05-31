import glob
import os
from shutil import copyfile
import pandas as pd

patient = "pat_2"
workdir = '{}/patients/{}{}'.format(os.getcwd(),patient,"/")
trees = glob.glob(workdir+"tree_*")
nbrOfTrees = len(trees)
allTerminal = False
terminals = []
stepTracker = 0
treeDepths = []

for i in range(0,len(trees)):
	nt = len(glob.glob('{}/patients/{}/tree_{}/*.png'.format(os.getcwd(),patient,i+1)))
	treeDepths.append(nt)

td = pd.DataFrame(treeDepths)

td.to_csv('{}/patients/{}/TreeLength.txt'.format(os.getcwd(),patient),index = False,header = False)

while(not(allTerminal)):
	os.mkdir(workdir + "step_" + str(stepTracker))
	for currTree in trees:
		if(currTree in terminals):
			currLen = len(glob.glob(currTree+"\\*.png"))
			copyfile(currTree+"\\patient_depth_"+str(currLen-1)+".png",
				workdir+"step_"+str(stepTracker)+"\\tree_"+str(currTree.split("tree_")[1])+"_step_"+str(stepTracker)+".png")
		else:
			copyfile(currTree+"\\patient_depth_"+str(stepTracker)+".png",
				workdir+"step_"+str(stepTracker)+"\\tree_"+str(currTree.split("tree_")[1])+"_step_"+str(stepTracker)+".png")
			currLen = len(glob.glob(currTree+"\\*.png"))
			if(currLen-1<=stepTracker):
				terminals.append(currTree)
	
	if(len(terminals)>=nbrOfTrees):
		allTerminal = True
	stepTracker += 1
	
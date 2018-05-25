import pandas as pd
import matplotlib.pyplot as plt
import glob

files = glob.glob("Output_Relation*.txt")
for k in range(0,len(files)):
	plt.clf()
	filename = files[k]
	data = pd.read_csv(filename,sep=" ",header = None, skiprows=1)

	nrows = data.shape[0]

	
	concentric = True

	if(concentric):
		if(nrows==2):
			fig, ax = plt.subplots(figsize=(9.0,6.0))
			plt.rcParams["font.size"]=13.0
			for i in range(0,nrows):
				sizes = data.iloc[i,1:3]
				ax.pie(sizes,radius=1-(0.4*(nrows-(i+1))),colors=["green","red"],wedgeprops=dict(width=0.4,edgecolor="w"),pctdistance=0.67+0.05*(i+1))
				ax.text(1-(0.4*(nrows-(i+1)))-0.4,0.05,str(data.iloc[i,0]),fontsize=13)

			ax.set(aspect="equal")
		else:
			fig, ax = plt.subplots(figsize=(12.0,9.0))
			plt.rcParams["font.size"]=13.0
			for i in range(0,nrows):
				sizes = data.iloc[i,1:3]
				ax.pie(sizes,radius=1-(0.2*(nrows-(i+1))),colors=["green","red"],wedgeprops=dict(width=0.2,edgecolor="w"),pctdistance=0.67+0.05*(i+1))
				ax.text(1-(0.2*(nrows-(i+1)))-0.2-(0.01*i),0.05+(0.09*i),str(data.iloc[i,0]),fontsize=13)

			ax.set(aspect="equal")

	else:
		plt.rcParams["font.size"]=13.0
		for i in range(0,nrows):

			sizes = data.iloc[i,1:3]
			if(nrows==2):
				iplot = 100+20+(i+1)
			elif(nrows==4):
				iplot = 200+20+(i+1)
			plt.subplot(iplot)
			plt.pie(sizes,colors=["green","red"],shadow=True,autopct='%1.1f%%',startangle = 90)
			if(nrows==2):
				plt.title(str(data.iloc[i,0]),fontdict=dict(fontsize=18),verticalalignment="top")
			else:
				plt.title(str(data.iloc[i,0]),fontsize=18)

			plt.axis("equal")
		plt.subplots_adjust(left=0.11,right=0.90,bottom=0.05,top=0.85,wspace=0.20)

	tp = open(filename,"r")

	plt.suptitle(next(tp),fontsize=25)
	plt.legend(["Good","Bad"],loc="lower right",bbox_to_anchor=(1.2,-0.05))
	#plt.show()
	plt.savefig(filename[:-4]+".png",format="png",dpi=200)
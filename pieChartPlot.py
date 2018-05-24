import pandas as pd
import matplotlib.pyplot as plt
filename = "Output_Relation_B_Age.txt"
data = pd.read_csv(filename,sep=" ",header = None, skiprows=1)

nrows = data.shape[0]

plt.rcParams["font.size"]=20.0

for i in range(0,nrows):

	sizes = data.iloc[i,1:3]
	if(nrows==2):
		iplot = 100+20+(i+1)
	elif(nrows==4):
		iplot = 200+20+(i+1)
	plt.subplot(iplot)
	plt.pie(sizes,labels=["Good","Bad"],colors=["green","red"],shadow=True,autopct='%1.1f%%',startangle = 90)
	plt.title(str(data.iloc[i,0]),fontsize=30)
	plt.axis("equal")


tp = open(filename,"r")

plt.suptitle(next(tp),fontsize=40)
plt.subplots_adjust(left=0.2,right=0.8,wspace=0.07)
plt.show()
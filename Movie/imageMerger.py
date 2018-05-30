import glob
import os
import math
import imageio
import pandas as pd
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
global newImSize

def mergeImages(imList,dir,patNo,data):

	global newImSize

	nrows = 6
	ncols = 6

	nbrOfImg = len(imList)
	new_im=Image.new('RGBA',newImSize,(255,255,255,255))

	x_steps = math.floor(newImSize[0]/ncols)
	y_steps = math.floor((newImSize[1]-150)/nrows)

	x_ind = 0
	y_ind = 0

	for i in range(0,nbrOfImg):
		im = Image.open(imList[i])
		width, height = im.size
		if width > math.floor(0.95*x_steps) and height > y_steps:
			im.thumbnail((math.floor(0.95*x_steps),y_steps))
			new_im.paste(im,(x_ind*x_steps,150+y_ind*y_steps))
		else:
			 xDiff = math.floor(0.95*x_steps)-width
			 yDiff = y_steps - height
			 new_im.paste(im,(x_ind*x_steps+max(math.floor(xDiff/2),0),150+y_ind*y_steps+max(0,math.floor(yDiff/2))))

		x_ind = x_ind + 1
		if(x_ind>=ncols):
			x_ind=0
			y_ind=y_ind+1


	age = data.iloc[patNo]["B_Age"]
	sex = data.iloc[patNo]["B_Sex"]
	if(sex==1):
		sex = "Female"
	else:
		sex = "Male"
	draw = ImageDraw.Draw(new_im)
	font = ImageFont.truetype("arialbd.ttf",72)
	draw.text((newImSize[0]/2-100,50),sex + ", " + str(int(age)),(0,0,0),font=font)		
	new_im.save(dir+"Merged Image.png")
	return(dir+"Merged Image.png")


noIm = 36
startind = 150
newImSize = [3000,2000]
patient = "pat_1"


workdir = '{}/patients/{}{}'.format(os.getcwd(),patient,"/")
patnr = int(patient.split("pat_")[1])
tp = glob.glob(workdir +"step_*")
nbrOfSteps = len(tp)
mergedImages = []
data = pd.read_excel("Imputed_Data.xlsx")

for i in range(0,nbrOfSteps):
	readDir = workdir + "step_" + str(i) + "\\"
	files = glob.glob(readDir + "tree_*.png")

	imName = mergeImages(files[startind:startind + noIm],readDir,patnr,data)
	mergedImages.append(imName)

images = []
for filename in mergedImages:
	images.append(imageio.imread(filename))

finalname = '{}/patients/{}/final/final_im.png'.format(os.getcwd(),patient)
im = Image.open(finalname)
tpim = Image.new('RGBA',newImSize,(255,255,255,255))
im2=im.resize([2000,1333])
tpim.paste(im2,(math.floor((newImSize[0]-2000)/2),math.floor((newImSize[1]-1333)/2)))

age = data.iloc[patnr]["B_Age"]
sex = data.iloc[patnr]["B_Sex"]
if(sex==1):
	sex = "Female"
else:
	sex = "Male"
draw = ImageDraw.Draw(tpim)
font = ImageFont.truetype("arialbd.ttf",72)
draw.text((newImSize[0]/2-100,50),sex + ", " + str(int(age)),(0,0,0),font=font)

tpim.save(finalname)
images.append(imageio.imread(finalname))
durations = list()
for i in range(0,len(images)-2):
	durations.append(1)
durations.append(4)
durations.append(4)

kargs={"duration":durations}
imageio.mimsave(workdir+"Movie.gif",images,"GIF-PIL",**kargs)
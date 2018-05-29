import glob
import os
import math
import imageio
import pandas as pd

def mergeImages(imList,dir,patNo,data):
	from PIL import Image
	from PIL import ImageFont
	from PIL import ImageDraw


	newImSize = [3000,2000]
	nrows = 4
	ncols = 5

	nbrOfImg = len(imList)
	new_im=Image.new('RGBA',newImSize,(255,255,255,255))

	x_steps = math.floor(newImSize[0]/ncols)
	y_steps = math.floor((newImSize[1]-150)/nrows)

	x_ind = 0
	y_ind = 0

	for i in range(0,nbrOfImg):
		im = Image.open(imList[i])
		im.thumbnail((x_steps-x_steps*0.05,y_steps))
		new_im.paste(im,(x_ind*x_steps,150+y_ind*y_steps))
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
	font = ImageFont.truetype("arial.ttf",56)
	draw.text((newImSize[0]/2-100,50),sex + ", " + str(int(age)),(0,0,0),font=font)		
	new_im.save(dir+"Merged Image.png")
	return(dir+"Merged Image.png")


noIm = 20
patient = "pat_0"


workdir = os.getcwd() + "\\" + patient
patnr = int(workdir.split("pat_")[1])
tp = glob.glob(workdir +"\\step_*")
nbrOfSteps = len(tp)
mergedImages = []
data = pd.read_excel("Imputed_Data.xlsx")

for i in range(0,nbrOfSteps):
	readDir = workdir + "\\step_" + str(i) + "\\"
	files = glob.glob(readDir + "tree_*.png")

	imName = mergeImages(files[0:noIm],readDir,patnr,data)
	mergedImages.append(imName)

images = []
for filename in mergedImages:
	images.append(imageio.imread(filename))

kargs={"duration":1}
imageio.mimsave(workdir+"\\Movie.gif",images,"GIF",**kargs)
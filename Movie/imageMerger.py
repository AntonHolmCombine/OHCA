import glob
import os
import math
import imageio

def mergeImages(imList,dir):
	from PIL import Image


	newImSize = [3000,2000]
	nrows = 4
	ncols = 5
	nbrOfImg = len(imList)
	new_im=Image.new('RGBA',newImSize,(255,255,255,255))

	x_steps = math.floor(newImSize[0]/ncols)
	y_steps = math.floor(newImSize[1]/nrows)

	x_ind = 0
	y_ind = 0

	for i in range(0,nbrOfImg):
		im = Image.open(imList[i])
		im.thumbnail((x_steps,y_steps))
		new_im.paste(im,(x_ind*x_steps,y_ind*y_steps))
		x_ind = x_ind + 1
		if(x_ind>=ncols):
			x_ind=0
			y_ind=y_ind+1


	new_im.save(dir+"Merged Image.png")
	return(dir+"Merged Image.png")


noIm = 18

tp = glob.glob(os.getcwd() +"\\step_*")
nbrOfSteps = len(tp)
mergedImages = []

for i in range(0,nbrOfSteps):
	readDir = os.getcwd() + "\\step_" + str(i) + "\\"
	files = glob.glob(readDir + "tree_*.png")

	imName = mergeImages(files[0:noIm],readDir)
	mergedImages.append(imName)

images = []
for filename in mergedImages:
	images.append(imageio.imread(filename))

kargs={"duration":1}
imageio.mimsave(os.getcwd()+"\\Movie.gif",images,"GIF",**kargs)
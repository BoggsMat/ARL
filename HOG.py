from PIL import Image
import cv2
import numpy as np 
import math


def loadImage(imname): 
	# Load image and resize
	im = cv2.imread(imname)
	im = cv2.resize(im, (128, 128))
	im = np.float32(im)/255.0; 
	return im

def fillHistogram(angle, mag, hist): 
	dist = (angle % 20) / 20
	upper =  mag * dist
	lower = mag * (1-dist)
	temp = (angle % 180) / 20
	lowbin = int(math.floor(temp))
	upbin = (int(math.ceil(temp))%9)
	hist[lowbin] += lower
	hist[upbin] += upper

def normalizeBlock(h1, h2, h3, h4): 
	sum = 0.0
	normalVector = np.zeros(36)

	for i in range(9): 
		sum += (h1[i]**2 + h2[i]**2 + h3[i]**2 + h4[i]**2)

	normal = sum**0.5

	for i in range(9):
		normalVector[i] = h1[i]/normal
		normalVector[i+9] = h2[i]/normal
		normalVector[i+18] = h3[i]/normal
		normalVector[i+27] = h4[i]/normal

	return normalVector

def concat(features, blocks):
	for block in blocks:
	 	for bin in block: 
			features.append(bin)

def HOG(im): 
	# Sobel 
	gx = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=1)
	gy = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=1)

	# Find magnitude and angle of sobel masks 
	mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)

	# Create array of histos 
	histograms = np.zeros((16,16,9))

	# Loop across every 8x8 block of pixels 
	xpos = 0
	ypos = 0

	for i in range(0, 16): 
		for j in range(0, 16): 
			for x in range(xpos, xpos + 8): 
				for y in range(ypos, ypos + 8): 
					fillHistogram(angle[xpos][ypos][0], mag[xpos][ypos][0], histograms[i][j] )	
			ypos += 8
			if ypos == 128:
				ypos = 0
				xpos += 8

	# Normalize 16x16 blocks
	blocks = [] 
	for r in range(0, 15):
		for c in range(0, 15):
			blocks.append(normalizeBlock(histograms[r][c], histograms[r][c+1], histograms[r+1][c], histograms[r+1][c+1]))

	# Concatenate the vectors 
	featureVector = []
	concat(featureVector, blocks)
	featureVector = np.array(featureVector)

	return featureVector
	
def main(): 
	im = loadImage('HOGim.jpg')
	HOG(im)

if __name__ == '__main__':
	main()












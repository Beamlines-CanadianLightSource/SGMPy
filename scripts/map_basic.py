import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import numpy as np

def getXRF(sgmData):

	print "Summing all XRF spectra."

	xrf1 = np.sum(sgmData[1], axis=0)
	xrf2 = np.sum(sgmData[2], axis=0)
	xrf3 = np.sum(sgmData[3], axis=0)
	xrf4 = np.sum(sgmData[4], axis=0)

	print "Plotting XRF."

	plt.figure(1)
	plt.subplot(221)
	plt.plot(xrf1)
	plt.subplot(222)
	plt.plot(xrf2)
	plt.subplot(223)
	plt.plot(xrf3)
	plt.subplot(224)
	plt.plot(xrf4)
	plt.show()

def plotpfyScatter(hex_x, hex_y, pfyData):
	plt.close('all')
	print "Making scatter plots."

	plt.figure(1)
	plt.subplot(221, aspect='auto')
	plt.scatter(hex_x, hex_y, c=pfyData[0], s=20, linewidths=0)
	print "Done MCA1."
	plt.subplot(222, aspect='auto')
	plt.scatter(hex_x, hex_y, c=pfyData[1], s=20, linewidths=0)
	print "Done MCA2."
	plt.subplot(223, aspect='auto')
	plt.scatter(hex_x, hex_y, c=pfyData[2], s=20, linewidths=0)
	print "Done MCA3."
	plt.subplot(224, aspect='auto')
	plt.scatter(hex_x, hex_y, c=pfyData[3], s=20, linewidths=0)
	print "Done MCA4."
	plt.show()

def plotCntScatter(hex_x, hex_y, counter):
	plt.close('all')
	color = counter
	plt.scatter(hex_x, hex_y, c=color, s=20, linewidths=0)

def plotpfyGrid(hex_x, hex_y, pfyData, xpts, ypts, shift):
	plt.close('all')
	print "Plotting grids."

	minX = min(hex_x)
	maxX = max(hex_x)
	minY = min(hex_y)
	maxY = max(hex_y)

	xi = np.linspace(minX,maxX,xpts)
	yi = np.linspace(minY,maxY,ypts)

        hex_x_ad = np.zeros((len(hex_x)))

	for i in range(1,len(hex_x)): 
		hex_x_ad[i] = hex_x[i] + shift*(hex_x[i] - hex_x[i-1])
	
	plt.figure(1)
	plt.subplot(221)
	print "Interpolating MCA1"
	zi1 = griddata(hex_x_ad, hex_y, pfyData[0], xi, yi, interp='linear')
	print "Done."
	plt.imshow(zi1)
	plt.subplot(222)
	print "Interpolating MCA2"
	zi2 = griddata(hex_x_ad, hex_y, pfyData[1], xi, yi, interp='linear')
	print "Done."
	plt.imshow(zi2)
	plt.subplot(223)
	print "Interpolating MCA3"
	zi3 = griddata(hex_x_ad, hex_y, pfyData[2], xi, yi, interp='linear')
	print "Done."
	plt.imshow(zi3)
	plt.subplot(224)
	print "Interpolating MCA4"
	zi4 = griddata(hex_x_ad, hex_y, pfyData[3], xi, yi, interp='linear')
	print "Done."
	plt.imshow(zi4)
	plt.show()

	return zi1, zi2, zi3, zi4

def plotpfyGridc(hex_x, hex_y, pfy_data, depth, shift):
	plt.close('all')
	print "Plotting contours."

	hex_x_ad = np.zeros((len(hex_x)))

	hex_x_ad[0] = hex_x[0]
        for i in range(1,len(hex_x)):
                hex_x_ad[i] = hex_x[i] + shift*(hex_x[i] - hex_x[i-1])

	plt.figure(1)
	plt.subplot(221)
	plt.tricontourf(hex_x_ad, hex_y, pfy_data[0], depth)
	plt.subplot(222)
	plt.tricontourf(hex_x_ad, hex_y, pfy_data[1], depth)
	plt.subplot(223)
	plt.tricontourf(hex_x_ad, hex_y, pfy_data[2], depth)
	plt.subplot(224)
	plt.tricontourf(hex_x_ad, hex_y, pfy_data[3], depth)
	plt.show()


def plotMap(filename,scanNum,pfylow,pfyhigh):

	f=openSGMSpec(filename, scanNum)
	g=getPFY(f,pfylow,pfyhigh)
	plotpfyGridc(f,g,500,0.75)

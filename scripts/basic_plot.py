# SGM Data view module

from praxes.io import spec
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import numpy as np

def openSGMSpec(sgmFile, scanNum):

	print "Opening scan", str(scanNum)
	print "in", sgmFile

	f = spec.open(sgmFile)
	scan=f[str(scanNum)]

	hex_x = scan['Hex_XP']
	mcadata=scan['@A1']

	print "Parsing MCAs"

	mca1=[]
	mca2=[]
	mca3=[]
	mca4=[]

	for i in range(0,len(hex_x)):
		mca1.append(mcadata[i*4])
		mca2.append(mcadata[i*4 + 1])
		mca3.append(mcadata[i*4 + 2])
		mca4.append(mcadata[i*4 + 3])

	print "Done!"
	return scan, mca1, mca2, mca3, mca4

def openSGMXAS(sgmFile, scanNum):

	print "Opening scan", str(scanNum)
	print "in", sgmFile

	f = spec.open(sgmFile)
	scan=f[str(scanNum)]

	energy = scan['Energy']	

	mcadata=scan['@A1']

	print "Parsing MCAs"

	mca1=[]
	mca2=[]
	mca3=[]
	mca4=[]

	for i in range(0,len(energy)):
		mca1.append(mcadata[i*4])
		mca2.append(mcadata[i*4 + 1])
		mca3.append(mcadata[i*4 + 2])
		mca4.append(mcadata[i*4 + 3])

	print "Done!"
	return scan, mca1, mca2, mca3, mca4


def openAllSGMXAS(sgmFile):
	f = spec.open(sgmFile)
	totalScanNum = len(f.keys())
	print "Total scan: ", totalScanNum
	scan=[]
	mca1=[[] for a in range(totalScanNum)]
	mca2=[[] for a in range(totalScanNum)]
	mca3=[[] for a in range(totalScanNum)]
	mca4=[[] for a in range(totalScanNum)]
    
	for j in range (0, totalScanNum):
		print 'index of the for loop is: ', j
		print 'Scan No.', j+1
		scan.append(f[str(j+1)])
		energy = scan[j]['Energy']	
		mcadata=scan[j]['@A1']

		print "Parsing MCAs"

		for i in range(0,len(energy)):
			mca1[j].append(mcadata[i*4])
			mca2[j].append(mcadata[i*4 + 1])
			mca3[j].append(mcadata[i*4 + 2])
			mca4[j].append(mcadata[i*4 + 3])
              
		print "Done!"

	return scan, mca1, mca2, mca3, mca4

def getPFY(sgmData, enStart, enStop):

	print "Getting PFY ROIs"

	pfy1=[]
	pfy2=[]
	pfy3=[]
	pfy4=[]

	for i in range(0, len(sgmData[1])):
		pfy1.append(np.sum(sgmData[1][i][enStart:enStop]))
		pfy2.append(np.sum(sgmData[2][i][enStart:enStop]))
		pfy3.append(np.sum(sgmData[3][i][enStart:enStop]))
		pfy4.append(np.sum(sgmData[4][i][enStart:enStop]))
	
	return pfy1, pfy2, pfy3, pfy4
	print "Done!"

def plotXAS_one(sgmData, pfyData, name):

	print "Plotting %s" %name

	en = sgmData[0]['Energy']
	data = sgmData[0][name]	
	
	plt.plot(en, data)
	plt.show()

def plotXAS_all(sgmData, pfyData):
	
	print "Plotting XAS."

	en = sgmData[0]['Energy']
	tey = sgmData[0]['TEY']
	i0 = sgmData[0]['I0']
	diode = sgmData[0]['Diode']

	plt.figure(1)
	plt.subplot(241)
	plt.plot(en, i0)
	plt.subplot(242)
	plt.plot(en, tey)
	plt.subplot(243)
	plt.plot(en, diode)
	plt.subplot(245)
	plt.plot(en, pfyData[0])
	plt.subplot(246)
	plt.plot(en, pfyData[1])
	plt.subplot(247)
	plt.plot(en, pfyData[2])
	plt.subplot(248)
	plt.plot(en, pfyData[3])
	plt.show()

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

def plotpfyScatter(scan, pfyData):

	print "Making scatter plots."

        hex_x = scan[0]['Hex_XP']
        hex_y = scan[0]['Hex_YP']

        plt.figure(1)
        plt.subplot(221, aspect='auto')
        plt.scatter(hex_x, hex_y, c=pfyData[0], s=2, linewidths=0)
	print "Done MCA1."
        plt.subplot(222, aspect='auto')
        plt.scatter(hex_x, hex_y, c=pfyData[1], s=2, linewidths=0)
	print "Done MCA2."
        plt.subplot(223, aspect='auto')
        plt.scatter(hex_x, hex_y, c=pfyData[2], s=2, linewidths=0)
	print "Done MCA3."
        plt.subplot(224, aspect='auto')
        plt.scatter(hex_x, hex_y, c=pfyData[3], s=2, linewidths=0)
	print "Done MCA4."
        plt.show()

def plotCntScatter(scan, counter):
        
	hex_x = scan[0]['Hex_XP']
        hex_y = scan[0]['Hex_YP']

	color = scan[0][counter]
	plt.scatter(hex_x, hex_y, c=color, s=2, linewidths=0)

def plotpfyGrid(scan, pfyData, xpts, ypts, shift):

	print "Plotting grids."
	hex_x = scan[0]['Hex_XP']
        hex_y = scan[0]['Hex_YP']

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

def plotpfyGridc(scan, pfyData, depth, shift):

        print "Plotting contours."
        hex_x = scan[0]['Hex_XP']
        hex_y = scan[0]['Hex_YP']

        hex_x_ad = np.zeros((len(hex_x)))

	hex_x_ad[0] = hex_x[0]
        for i in range(1,len(hex_x)):
                hex_x_ad[i] = hex_x[i] + shift*(hex_x[i] - hex_x[i-1])

	plt.figure(1)
        plt.subplot(221)
        plt.tricontourf(hex_x_ad, hex_y, pfyData[0], depth)
        plt.subplot(222)
        plt.tricontourf(hex_x_ad, hex_y, pfyData[1], depth)
        plt.subplot(223)
        plt.tricontourf(hex_x_ad, hex_y, pfyData[2], depth)
        plt.subplot(224)
        plt.tricontourf(hex_x_ad, hex_y, pfyData[3], depth)
        plt.show()


def plotMap(filename,scanNum,pfylow,pfyhigh):

	f=openSGMSpec(filename, scanNum)
	g=getPFY(f,pfylow,pfyhigh)
	plotpfyGridc(f,g,500,0.75)

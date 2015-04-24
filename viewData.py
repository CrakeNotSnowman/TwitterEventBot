#!/usr/bin/env python

'''
Keith Murray

This is to plot and visualize the data recorded in the [event].txt files
'''
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import math

def plotEvent(eventF):
    eventHistory = open(str(eventF) + ".txt", 'r')
    theTimes = []
    theAvgs = []
    theVar = []
    for line in eventHistory:
	if line == "":
	    break
	line = line.split('\t')
	theTimes.append(line[0])
	theAvgs.append(1/float(line[1]))
	theVar.append(float(line[2]))

    eventHistory.close()
    dates = theTimes
    x = np.array([dt.datetime.strptime(d,'%Y-%m-%d %H:%M') for d in dates])
    
    '''
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    #plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())
    plt.plot(x,theAvgs)
    plt.gcf().autofmt_xdate()
    plt.show()
    plt.close()
    '''
    plt.figure(1)
    ax1 = plt.subplot(211)
    plt.title(eventF[0].upper() + eventF[1:].lower())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    #plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())
    plt.gcf().autofmt_xdate()
    ax1.plot(x,theAvgs)
    plt.ylabel("Average Tweets Per Second")
    ax2 = plt.subplot(212, sharex=ax1)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    #plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())
    ax2.plot(x,theVar)
    plt.gcf().autofmt_xdate()
    plt.ylabel("Variance of \nthe Average")

    plt.show()
    plt.close()

    # look to see
    #  1: how the current average compares to the old avg of the std of old avg
    #  2: how the old average compares to the current avg and std

    histAvg = [theAvgs[0]]
    zSc1 = [0]
    zSc2 = [0]
    for i in range(1,len(theAvgs)):
	curAvg = theAvgs[i]
	curVar = theVar[i]
	curStd = math.sqrt(curVar)
	oldAvg = np.mean(histAvg)
	oldStd = np.std(histAvg)
	histAvg.append(curAvg)
	zSc1.append((curAvg - oldAvg)/oldStd)
	zSc2.append((oldAvg - curAvg)/curStd)

    plt.figure(2)
    ax1 = plt.subplot(211)
    plt.title(eventF[0].upper() + eventF[1:].lower())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    #plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())
    plt.gcf().autofmt_xdate()
    ax1.plot(x,zSc1)
    plt.ylabel("Current set of tweets wrt \nthe past averages and std")
    ax2 = plt.subplot(212, sharex=ax1)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    #plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())
    ax2.plot(x,zSc2)
    plt.gcf().autofmt_xdate()
    plt.ylabel("Past Average compared to the average\n current set and the std of that set")

    plt.show()
    plt.close()


    
    return
def main(eventF):
    eventList = open("listOfTwitterEvents.txt", 'r')
    eL = []
    for line in eventList:
	eL.append(str(line))
    print "*********************************"
    while True:
	for i in range(len(eL)):
	    print "*\t ",eL[i].strip(), "\t\t*"
	eventF = raw_input("* Please enter the event name:  *\n\t")
	for i in range(len(eL)):
	    tempE = eL[i].strip()
	    if eventF.lower() == tempE.lower():
		eventF = tempE
	try:
	    plotEvent(eventF)
	except IOError:
	    pass

main('earthquake')
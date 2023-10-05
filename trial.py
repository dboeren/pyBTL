from pyBTLtypes import damageRec, attackResults
from sim import *
import numpy as np
import copy
import threading
import matplotlib.pyplot as plt
import math

# the main function
def runSim(attacks, lock, damage, burncap, trials, threadNum, label):

    threads = []
    dataMain = []
    tbn = getTrialsByThread(trials, threadNum)

    for n in tbn:

        data = np.empty(n, dtype=object)
        dataMain.append(data)
        thread = threading.Thread(target=simThread,args=(attacks, lock, damage, burncap,data))
        threads.append(thread)

    for thread in range(threadNum):
        threads[thread].start()

    for thread in range(threadNum):
        threads[thread].join()

    # splice together results
    dataAll = np.concatenate(dataMain)

    dataA2 = np.zeros(trials, dtype=int)
    dataA3 = np.zeros(trials, dtype=int)
    dataA4 = np.zeros(trials, dtype=int)
    dataA5 = np.zeros(trials, dtype=int)
    dataA6 = np.zeros(trials, dtype=int)
    dataS = np.zeros(trials, dtype=int)

    # to do - copy per-armor results from dataAll elements to data arrays

    maxDamage = damage * burncap

    binRng = range(maxDamage + 1)

    dataA2 = []
    dataA3 = []
    dataA4 = []
    dataA5 = []
    dataA6 = []
    dataS = []

    # extract the per-armor data into arrays
    te1 = threading.Thread(target=armorHist, args=(dataAll,  0, maxDamage, dataA2))
    te1.start()

    te2 = threading.Thread(target=armorHist, args=(dataAll,  1, maxDamage, dataA3))
    te2.start()

    te3 = threading.Thread(target=armorHist, args=(dataAll,  2, maxDamage, dataA4))
    te3.start()

    te4 = threading.Thread(target=armorHist, args=(dataAll,  3, maxDamage, dataA5))
    te4.start()

    te5 = threading.Thread(target=armorHist, args=(dataAll,  4, maxDamage, dataA6))
    te5.start()

    te6 = threading.Thread(target=armorHist, args=(dataAll, 5, maxDamage, dataS))
    te6.start()

    te1.join()
    te2.join()
    te3.join()
    te4.join()
    te5.join()
    te6.join()



    plt.plot(binRng, dataA2[0], label = "2+ sv")
    plt.plot(binRng, dataA3[0], label = "3+ sv")
    plt.plot(binRng, dataA4[0], label = "4+ sv")
    plt.plot(binRng, dataA5[0], label = "5+ sv")
    plt.plot(binRng, dataA6[0], label = "6+ sv")
    plt.plot(binRng, dataS[0], label = "Shlds")
    plt.legend()
    plt.title(label)
    plt.xlabel("Damage")
    plt.ylabel("Percent Chance")
    plt.grid(visible=True)
    plt.show()

    

# function run by threads
def simThread(attacks, lock, damage, burncap, storage):

    for index in range(len(storage)):
        storage[index] = btlSim(attacks, lock, damage, burncap)


# allocates a number of trials to each thread
def getTrialsByThread(trials, threadNum):

    tbn = np.zeros(threadNum,dtype=int)

    remainingTrials = copy.copy(trials)

    tpt = math.ceil(trials / threadNum)

    for index in range(len(tbn)):

        if remainingTrials > tpt:

            tbn[index] = tpt
            remainingTrials -= tpt
        else:
            tbn[index] = remainingTrials

    return tbn

# takes damage for a single armor save stat out of the packed storage array, places it in a dedicated array and then histograms it
def armorHist(damage, index, maxDamage, output):

    samples = len(damage)

    storage = np.zeros(samples, dtype=int)

    for i in range(len(damage)):
        val = damage[i].data[index]
        storage[i] = val

    data = np.zeros(maxDamage+1, dtype=int)

    # would have preferred to use a np stat function here but they were being annoying
    for element in storage:
        data[element] += 1

    # normalize
    for i in range(len(data)):
        data[i] = data[i] / samples * 100

    output.append(data)



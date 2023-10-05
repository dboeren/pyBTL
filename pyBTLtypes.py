import numpy as np
import random as rng

class attackResults:

    def __init__(self, setHits = 0, setCrits = 0):
        self.hits = setHits
        self.crits = setCrits

    def total(self):
        return self.hits + self.crits

class damageRec:
    def __init__(self):
        self.data = np.zeros(6)

    def crit(self, num):
        self.data[0] += num
        self.data[1] += num
        self.data[2] += num
        self.data[3] += num
        self.data[4] += num

    def saveFail(self, arm):
        self.data[arm-2] += 1

    def shieldSaveCrit(self):
        roll = rng.randint(0,1)

        if roll > 0:
            self.data[5] += 1

    def shieldSave(self, roll):

        if roll >= 4 :
            self.data[5] += 1

    def armorSave(self, roll):
        savesFailed = range(roll - 1,5)

        for armor in savesFailed:
            self.data[armor] += 1
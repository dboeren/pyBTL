from pyBTLtypes import damageRec, attackResults
import numpy as np
import copy
import random as rng

# this file does the actual mechanics of simulating BTL attacks

# an individual BTL attack
def btlSim(attacks, lock, damage, burncap, isBtl, isParticle, isHeavyCal):

    simAttacks = [copy.copy(attacks)]
    
    damageTracker = attackResults()

    autocrit = [False]

    if (isParticle):
        autocrit = [True]

    run = True

    while run:
        run = attackStep(simAttacks, lock, damage, burncap, damageTracker, autocrit, isHeavyCal)
        if (not isBtl):
            run=False

    return armor(damageTracker)


def attackStep(attacks, lock, damage, burncap, damageTracker, autocrit, isHeavyCal):
    rolls = np.zeros(attacks[0])

    for i in range(attacks[0]):
        rolls[i] = rng.randint(1,6)

    rolls.sort()
    rolls = np.flip(rolls)

    misses = 0

    if autocrit[0]:
        for roll in rolls:
            if roll >= lock:
                damageTracker.crits += damage
            elif roll < lock:
                misses += 1
            if damageTracker.total() >= burncap:
                return False
    else:
        for roll in rolls:
            if roll >= lock + 2:
                autocrit[0] = True
                damageTracker.crits += damage
            elif (roll >= lock + 1) and isHeavyCal:
                autocrit[0] = True
                damageTracker.crits += damage
            elif roll >= lock:
                damageTracker.hits += damage
            elif roll < lock:
                misses += 1

            if damageTracker.total() >= burncap:
                return False

    if misses > 0:
        attacks[0] = attacks[0] - misses
        if attacks[0] == 0:
            return False
    
    return True

# rolls armor saves and applies damage to armor damage accumulators
def armor(damageTracker):

    damageResults = damageRec()

    damageResults.crit(damageTracker.crits)

    # shield saves against crits
    for dmg in range(damageTracker.crits):
        damageResults.shieldSaveCrit()

    # armor and shield saves against hits
    for dmg in range(damageTracker.hits):
        roll = rng.randint(1,6)
        damageResults.armorSave(roll)
        damageResults.shieldSave(roll)

    return damageResults


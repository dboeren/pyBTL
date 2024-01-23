import tkinter as tk
import sys
from trial import runSim

mainWindow = tk.Tk()
mainWindow.title("pyBTL")

nameFrame = tk.Frame(mainWindow)
nameLabel = tk.Label(nameFrame, text="Name")
nameLabel.pack(side=tk.LEFT)
nameEntry = tk.Entry(nameFrame)
nameEntry.pack(side=tk.LEFT)
nameFrame.pack(side=tk.TOP)

tOpts = [1,2,4,8]
nOpts = [1000,10000,100000,1000000]

simFrame = tk.Frame(mainWindow)
threadsLabel = tk.Label(simFrame, text="Threads: ")
threadsLabel.pack(side=tk.LEFT)
tVar = tk.IntVar()
tVar.set(1)
nVar = tk.IntVar()
nVar.set(1000)
threadDrop = tk.OptionMenu(simFrame, tVar, *tOpts)
threadDrop.pack(side=tk.LEFT)
sampleLabel = tk.Label(simFrame, text="Trials: ")
sampleLabel.pack(side=tk.LEFT)
sampleDrop = tk.OptionMenu(simFrame, nVar, *nOpts)
sampleDrop.pack(side=tk.LEFT)
simFrame.pack(side=tk.BOTTOM)

# Add a frame for some checkbox options
checkboxFrame = tk.Frame(mainWindow)

btlVar = tk.IntVar()
btlButton = tk.Checkbutton(checkboxFrame, text='BTL', onvalue=1, offvalue=0, variable=btlVar)
btlButton.pack(side=tk.LEFT)

particleVar = tk.IntVar()
particleButton = tk.Checkbutton(checkboxFrame, text='Particle', onvalue=1, offvalue=0, variable=particleVar)
particleButton.pack(side=tk.LEFT)

heavycalVar = tk.IntVar()
heavycalButton = tk.Checkbutton(checkboxFrame, text='HeavyCal', onvalue=1, offvalue=0, variable=heavycalVar)
heavycalButton.pack(side=tk.LEFT)

checkboxFrame.pack(side=tk.TOP)


lockFrame = tk.Frame(mainWindow)
lockLabel = tk.Label(lockFrame, text="Lock")
lockSpin = tk.Spinbox(lockFrame, from_=2, to=6)
lockLabel.pack()
lockSpin.pack()
lockFrame.pack(side=tk.LEFT)

attackFrame = tk.Frame(mainWindow)
attackLabel = tk.Label(attackFrame, text="Attacks")
attackSpin = tk.Spinbox(attackFrame, from_=0, to=sys.maxsize)
attackLabel.pack()
attackSpin.pack()
attackFrame.pack(side=tk.LEFT)

damageFrame = tk.Frame(mainWindow)
damageLabel = tk.Label(damageFrame, text="Damage")
damageSpin = tk.Spinbox(damageFrame, from_=0, to=sys.maxsize)
damageLabel.pack()
damageSpin.pack()
damageFrame.pack(side=tk.LEFT)

btlFrame = tk.Frame(mainWindow)
btlLabel = tk.Label(btlFrame, text="Burn Cap")
btlSpin = tk.Spinbox(btlFrame, from_=0, to=sys.maxsize)
btlLabel.pack()
btlSpin.pack()
btlFrame.pack(side=tk.LEFT)

simButton = tk.Button(simFrame,text="Run", command = lambda : runSim(int(attackSpin.get()), int(lockSpin.get()), int(damageSpin.get()), int(btlSpin.get()), nVar.get(), tVar.get(), nameEntry.get(), int(btlVar.get()), int(particleVar.get()), int(heavycalVar.get()) ))
simButton.pack(side=tk.LEFT)
simFrame.pack(side=tk.BOTTOM)

mainWindow.mainloop()


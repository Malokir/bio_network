import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import random
import sys
import simu
import os


                                                    #PARAMETERS

p = {

    #distance
    "size":0.4,         #Dimension of the grid [m]
    "dx":10**(-3),      #Size of a pixel [m]
    #time
    "total_time":20,     #Duration of the study [s]
    "dt":1,             #Time step for elongation/division process [s]
    #angle
    "dteta":np.radians(40), #Division process: opening angle = 2*dteta [rad]
    "trunc":np.radians(70), #The difference between old and new angle during elong process cannot be greater than trunc°
    #concentration
    "b0":500.0,           #Inital concentration in the grid [concentration]
    "c0":250,           #Hill reference for consumption [concentration]
    "anni":442,         #Minimum concentration of chemical before inactivation of an active particle
    #Chemical behaviour
    "D":2.5*10**(-7),     #Diffusion coeff for chemical [m²/s]
    "cmax":2700,         #max consumption of chemical by unit of time  [concentration/s]
    #Particles behaviour
    "Dr":0.5,           #Rotation diffusion coeff for active particles [1/s]
    "sigma":0.4,         #Division rate [1/s]
    "v0":10**-2,        #Active particle speed [m/s]
    #Other
    "n":50,             # n * dt_diffusion = dt
}

                                                    #PECLET NUMBERS
Pcl = [p["v0"]/np.sqrt(p["n"]*p["D"]*p["Dr"]),p["sigma"]/p["Dr"]]


                                                    #INSTRUCTIONS                                           

dvp = 1             #choose 1 to show in live the network development. 0 otherwise
result = 1          #choose 1 to show the result when the development ends. 0 otherwise
save = 0            #choose 1 to save the network as an image
nsimu=1             #numer of different networks you want to develop in a row
                    #When save = 1, choose dvp=0 and result=0
                    #Each time save is set to 1, it creates a new folder, which number is doss_var. Change this variable each time.
                    #Each time save is set to 1, the parameters will be saved in the same folder as a text file.

                                                    #FILE CREATION
doss_var = 1
dossier = "Simu" + str(doss_var)
if save ==1:
    os.makedirs(dossier)

                                                    #RUN AND SAVE IMAGES
dead=0      #death counter
alive=0     #surviving counter
active=0
for i in range(nsimu):
    file="img" + str(i) +".jpg"
    res,act=simu.simu_func(p,dvp,result,save,dossier,file)
    active+=act
    if res=='dead':
        dead+=1
    else:
        alive+=1
    
                                                    #SAVE PARAMETERS
if save ==1:
    p["Pcl1"] = Pcl[0]
    p["Pcl2"] = Pcl[1]
    p["Survival rate"] = alive/(alive+dead)
    mean_active=active/nsimu
    p["survivng branch(mean)"] = mean_active

    file = 'parameters.txt' 
    path = os.path.join(dossier, file)
    with open(path, 'w') as file:
        for cle, valeur in p.items():
            file.write(f"{cle}: {valeur}\n")

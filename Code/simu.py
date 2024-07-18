import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import random
import sys
import t_f
import os

def simu_func(p,dvp,result,save,dossier,file):
                                                    #VARIABLES

    var = {
        "size_pix":int(p["size"]/p["dx"]),  #Size of the grid [pixel]
        "alpha":np.sqrt(2*p["Dr"]*p["dt"]), #Angular noise amplitude [1]
        "p":p["sigma"]*p["dt"],             #Probability of a branch to split for every dt [1]
        "d":p["v0"]*p["dt"]/p["dx"],        #Elongation distance for 1 time step dt [pixel]
    }
    var["xi"] = int(var["size_pix"]/2)      #Starting point [pixel]
    var["yi"] = int(var["size_pix"]/2)      #Starting point [pixel]
    

                                                    #PHYSICS CHECK
    if p["D"]*p["dt"]/p["dx"]**2 >= 1:
        print('diffusion factor = ', p["D"]*p["dt"]/p["dx"]**2, '> 0.25')    # convergence of finite differences method
        sys.exit(1)

    if var["p"] > 1:
        print('division probability = ', var["p"], '> 1')
        sys.exit(1)

    if var["d"] < 6:
        print('d = ',var["d"],' <=6')                      #continous background compared to particles motion
        sys.exit(1)
        
                                                    #INITIALISATION

    b=np.full((var["size_pix"],var["size_pix"]),p["b0"])
    b_next=b[:]
    active_centers = [(var["xi"], var["yi"], 0),(var["xi"], var["yi"], np.radians(120)),(var["xi"], var["yi"], np.radians(-120))]
    centros_consumidores=[]

    #centros_consumidores=[(var["xi"],var["yi"])]

    fig, ax = plt.subplots()
    img = ax.imshow(b, interpolation='nearest')
    plt.colorbar(img, ax=ax)
    
                                                    #RUN PROCESS
    survival = 'alive'
    branch_num=1
    for t in range(p["total_time"]):
        copy = active_centers.copy()
        random.shuffle(copy)
        if t==1:
            centros_consumidores.append((var["xi"],var["yi"]))

        #BRANCHING PROCESS
        for center in copy:
            dé = np.random.rand()
            #elongacion
            if dé > var["p"]:
                teta_previous = center[2]
                if t_f.local_measure(int(center[0]),int(center[1]),1,b) > p["anni"]:
                    teta_new = teta_previous + var["alpha"]*t_f.trunc_gauss(var["alpha"],p['trunc'])
                    new_center = t_f.new_cell(center, teta_new, var["d"]) + (teta_new,)
                    active_centers.append(new_center)
                    centros_consumidores.append((int(new_center[0]),int(new_center[1])))
                    t_f.disque_r(ax, new_center,var["d"])
                    ax.plot([center[1], new_center[1]], [center[0], new_center[0]], color='black',linewidth=var["d"]/20)
                t_f.disque_b(ax, center,var["d"])
                active_centers.remove(center)



            #division
            else:
                teta_previous = center[2]
                if t_f.local_measure(int(center[0]),int(center[1]),1,b) > p["anni"]:
                    branch_num+=1
                    teta_new1 = teta_previous + p["dteta"] + var["alpha"]/4*t_f.trunc_gauss(var["alpha"],p['trunc'])
                    teta_new2 = teta_previous - p["dteta"] + var["alpha"]/4*t_f.trunc_gauss(var["alpha"],p['trunc'])
                    new_center1 = t_f.new_cell(center, teta_new1, var["d"])
                    new_center2 = t_f.new_cell(center, teta_new2, var["d"])
                    active_centers.append(new_center1 + (teta_new1,))
                    active_centers.append(new_center2 + (teta_new2,))
                    centros_consumidores.append((int(new_center1[0]),int(new_center1[1])))
                    centros_consumidores.append((int(new_center2[0]),int(new_center2[1])))
                    t_f.disque_r(ax, new_center1,var["d"])
                    t_f.disque_r(ax, new_center2,var["d"])
                    ax.plot([center[1], new_center1[1]], [center[0], new_center1[0]], color='black',linewidth=var["d"]/20)
                    ax.plot([center[1], new_center2[1]], [center[0], new_center2[0]], color='black',linewidth=var["d"]/20)
                t_f.disque_b(ax, center,var["d"])
                active_centers.remove(center)
                #centros_consumidores.remove((int(center[0]),int(center[1])))


                #UPDATE BACKGROUND (diffusion)
        for _ in range(p["n"]):
            b_next[1:,:] += (b[:-1,:]- b[1:,:])*p["D"]*p["dt"]/p["dx"]**2
            b_next[:-1,:] += (b[1:,:]- b[:-1,:])*p["D"]*p["dt"]/p["dx"]**2
            b_next[:,1:] += (b[:,:-1] - b[:,1:])*p["D"]*p["dt"]/p["dx"]**2
            b_next[:,:-1] += (b[:,1:] - b[:,:-1])*p["D"]*p["dt"]/p["dx"]**2
            #doing that, the dt relative to diffusion is n times smaller than the dt relative to elongation

            for (i,j) in centros_consumidores:
                b_next[i,j] -= p["cmax"]*p["dt"]/p["n"]*t_f.Hill(b[int(i),int(j)]/p["c0"]) #because the consumption duration is dt/n (inside the for loop)



            b[:]=b_next[:]
            
        if len(active_centers)==0:
            survival = 'dead'
            break
            
        
        img.set_data(b)
        ax.set_title('Time {}'.format(t))
        ax.set_xlim(0, var["size_pix"])
        ax.set_ylim(0, var["size_pix"])
        img.set_clim(0, p["b0"])
        if dvp==1:
            fig.canvas.draw()
            plt.pause(0.05)
    if result == 1:
        plt.show()
    if save ==1:
        path = os.path.join(dossier, file)
        plt.savefig(path, format='jpeg', bbox_inches='tight',dpi=1200)
        plt.close(fig)
    return(survival,len(active_centers)/branch_num)
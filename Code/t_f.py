import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import random
import sys

def new_cell(previous_cell, teta, dist):
    #attention le teta est le nouveau et non l'ancien
    x0, y0 = previous_cell[0], previous_cell[1]
    x = x0 + dist * np.cos(teta)
    y = y0 + dist * np.sin(teta)
    return (x,y)

def disque_b(ax, centre,d):
    x,y=centre[0:2]
    cercle = Circle((y,x), int(d/5), color='blue', alpha=0.5)
    #the radius of the square is d/5
    ax.add_patch(cercle)

def disque_r(ax, centre,d):
    x,y=centre[0:2]
    cercle = Circle((y,x), int(d/5), color='red', alpha=0.5)
    ax.add_patch(cercle)


def Hill(x):
    return x**2/(1+x**2)

def local_measure(x,y,d,b):
    #si on veut faire un carré de (2d+1)^2 autour de x,y
    c=0
    for i in range(-d,d+1):
        for j in range(-d,d+1):
            c=c+b[x+i,y+j]
    res=c/((2*d+1)**2)
    #print(res)
    return res

def trunc_gauss(alpha,trunc):     #gaussienne centrée normée, de sorte que la diff entre l'ancien et le nouvel angle soit inférieure à trunc°
    res=np.random.normal(0,1)
    while abs(alpha*res) > trunc:
        res=np.random.normal(0,1)
    return res
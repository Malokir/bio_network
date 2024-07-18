# bio_network
Numerical modelling of a branched cell network development interacting with a diffusive chemical gradient.

ABSTRACT : 
Cellular networks in animal organs seem to fill space remarkably efficiently: they leave no empty space, while creating no intersections between branches. In order to understand the associated mechanisms, numerical modelling of such a phenomenon is a favoured avenue. However, current models, some of which do provide satisfactory results in terms of the final architecture of networks, remain imperfect in terms of their methodology. In fact, the annihilation process (the one that stops the development of a branch before it intersects with another) does not seem to be consistent with the biological behaviour of cells. 
This study proposes that it is a chemical interaction between branching cells and their environment that enables them to avoid collisions. It proposes a numerical model and then studies it. 

In 'Paper.pdf' you can find the research report corresponding to this study.
In the folder 'Code' are three Python files: t_f.py contains the tool functions used in simu.py ; simu.py allows the simulation of the development of a single network and is used in mult_simu.py ; mult_simu.py allows the simulation of various networks in a row, in order to simplify the study of the influences of the various parameters on the development of a network. 
Results.xlsx contains the data used in the analisis (last part of the paper).

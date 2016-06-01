import glob
import os
import sys
import code
import numpy as np
import mcubes


l = glob.glob("./knossTest/*")



#for ii in l:
ii = l[1]
f = open(ii, 'rb')
x = np.fromfile(f, dtype=np.int16)
mat = x.reshape(128, 128, 128)

first = ii.split("_")
x_cube = int(first[4][1:])
y_cube = int(first[5][1:])
z_cube = int(first[6].split('.')[0][1:])
code.interact(local=locals())

vertices, triangles = mcubes.marching_cubes(mat, 0)
#if len(vertices) == 0:
#    continue

#might need to transpose these
vertices[:,0] += 128 * z_cube
vertices[:,1] += 128 * y_cube
vertices[:,2] += 128 * x_cube



mcubes.export_mesh(vertices, triangles, ii + '.dae', "MySphere")

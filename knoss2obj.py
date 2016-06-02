import glob
import os
import sys
import code
import numpy as np
import mcubes


def writeOBJ(name, verts ,tris):
    f = open(name, 'w')
    for each in verts:
        f.write('v ' + str(each[0]) + ' ' + str(each[1]) + ' ' + str(each[2])+ '\r\n')
        #code.interact(local=locals())
    for each in tris:
        f.write('f ' + str(each[0]+1) + ' ' + str(each[1]+1) + ' ' + str(each[2]+1) + '\r\n')
    f.close()

l = glob.glob("./big/*.raw")


verts = []
for ii in l:
    f = open(ii, 'rb')
    x = np.fromfile(f, dtype=np.int16)
    f.close()
    mat = x.reshape(128, 128, 128)

    first = ii.split("_")
    x_cube = int(first[4][1:])
    y_cube = int(first[5][1:])
    z_cube = int(first[6].split('.')[0][1:])


    vertices, triangles = mcubes.marching_cubes(mat, 0)
    if len(vertices) == 0:
        continue

#might need to transpose these
    vertices[:,0] += 128 * z_cube
    vertices[:,1] += 128 * y_cube
    vertices[:,2] += 128 * x_cube

    #verts = [verts vertices]

    #code.interact(local=locals())
    writeOBJ(ii + '.obj', vertices, triangles)
    #code.interact(local=locals())

    #mcubes.export_mesh(vertices, triangles, ii + '.dae', "MySphere")

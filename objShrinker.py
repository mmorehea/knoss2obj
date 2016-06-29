from subprocess import call
from shutil import copyfile
import glob
import os

obj_path = '/home/curie/NathanCode/knoss2obj/obj/*.obj'
small_obj_path = '/home/curie/NathanCode/knoss2obj/small_obj/*.obj'

for obj in glob.glob(obj_path):

    small_objs = glob.glob(small_obj_path)
    for small_obj in small_objs:
        small_obj = small_obj[:-10]

    if obj[:-4] in small_objs:
        continue

    command1 = "meshlabserver -i " + obj + " -o " + obj[:-4] + "_temp.obj -s stretch.mlx"
    command2 = "meshlabserver -i " + obj[:-4] + "_temp.obj -o " + obj[:-4] + "_temp.obj -s deci.mlx"

    call(command1, shell=True)
    while os.path.getsize(obj[:-4] + "_temp.obj") > 1000000:
        call(command2, shell=True)

    name = (obj.split("/"))[-1]
    copyfile(obj[:-4] + "_temp.obj", '/home/curie/NathanCode/knoss2obj/small_obj/' + name[:-4] + "_small.obj")
    os.remove(obj[:-4] + "_temp.obj")


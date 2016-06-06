import code
import fnmatch
import glob
import matlab.engine
import os
import zipfile as zf

zips = []
dropbox_path = '/home/curie/knoss2obj/Webknossos/'
data_path = '/home/curie/knoss2obj/data/'
obj_path = '/home/curie/knoss2obj/obj/'
nrrd_path = '/home/curie/knoss2obj/obj/'
print('Starting matlab engine...')
eng = matlab.engine.start_matlab()

# Grab zipped raws from Dropbox, store in zips
print('Gathering zipped raw files...')

for root, dirnames, filenames in os.walk(dropbox_path, followlinks=True):
    for filename in fnmatch.filter(filenames, '*.zip'):
        zips.append(os.path.join(root, filename))

# Extract raws from each zip and convert to obj
names = []
for i in range(len(zips)):
    raws_to_delete = glob.glob('data/*.raw')
    for raw in raws_to_delete:
        os.remove(raw)
    names.append(zips[i].split('/')[len(zips[i].split('/'))-1][:-4])
    print('Converting {}...  {} of {}'.format(names[i], i+1, len(zips)))

    # Skip raw set if corresponding obj/nrrd already exists
    current_obj_path = obj_path + '/' + names[i] + '.obj'
    current_obj_name = 'obj/' + names[i] + '.obj'
    current_nrrd_path = nrrd_path + '/' + names[i] + '.nrrd'
    current_nrrd_name = 'nrrd/' + names[i] + '.nrrd'

    if current_obj_name in glob.glob('obj/*.obj') and current_nrrd_name in glob.glob('nrrd/*.nrrd'):
        print('Raw set {} is already up to date.'.format(i+1))
        continue
    current_zip = zf.ZipFile(zips[i])
    current_zip.extractall(data_path)
    success = eng.start(names[i])

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
    print('Converting raw set to obj: {} of {}'.format(i+1, len(zips)))
    raws_to_delete = glob.glob('data/*.raw')
    for raw in raws_to_delete:
        os.remove(raw)
    names.append(zips[i].split('/')[len(zips[i].split('/'))-1][:-4])

    # Skip raw set if corresponding obj already exists and is finished
    current_obj_path = obj_path + '/' + names[i] + '.obj'
    current_obj_name = 'obj\\' + names[i] + '.obj'

    # Broken
    if current_obj_name in glob.glob('obj\*.obj') and os.path.getmtime(zips[i]) > os.path.getmtime(current_obj_path):
        print('Raw set {} is already up to date.'.format(i+1))
        continue
    current_zip = zf.ZipFile(zips[i])
    current_zip.extractall(data_path)
    success = eng.start(names[i])
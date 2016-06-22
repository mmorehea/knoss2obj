import code
import fnmatch
import glob
import matlab.engine
import os
import pickle
import zipfile as zf


def clear_raws():
    raws_to_delete = glob.glob('/home/curie/NathanCode/knoss2obj/data/*.raw')
    for raw in raws_to_delete:
        os.remove(raw)

# Set paths, start engine
zips = []
names = []
dropbox_path = '/media/curie/5TB/Dropbox/WebKnossos/'
data_path = '/home/curie/NathanCode/knoss2obj/data/'
obj_path = '/home/curie/NathanCode/knoss2obj/obj/'
nrrd_path = '/media/curie/5TB/Dropbox/KnossNrrds/'
print('Starting matlab engine...')
eng = matlab.engine.start_matlab()
eng.cd('/home/curie/NathanCode/knoss2obj/')

# Clean up outdated nrrds and objs
zipcheck = []
nrrdcheck = []
objcheck = []
for root, dirnames, filenames in os.walk(dropbox_path, followlinks=True):
    for filename in fnmatch.filter(filenames, '*.zip'):
        zipcheck.append(filename)
for root, dirnames, filenames in os.walk(nrrd_path, followlinks=True):
    for filename in fnmatch.filter(filenames, '*.nrrd'):
        nrrdcheck.append(filename)
for root, dirnames, filenames in os.walk(obj_path, followlinks=True):
    for filename in fnmatch.filter(filenames, '*.obj'):
        objcheck.append(filename)
for nrrd2check in nrrdcheck:
    found = False
    for zip2check in zipcheck:
        if nrrd2check[:-5] == zip2check[:-4]:
            found = True
    if not found:
        os.remove(os.path.join(nrrd_path, nrrd2check))
for obj2check in objcheck:
    found = False
    for zip2check in zipcheck:
        if obj2check[:-4] == zip2check[:-4]:
            found = True
    if not found:
        os.remove(os.path.join(obj_path, obj2check))

# Load modtimes from pickle
if '/home/curie/NathanCode/knoss2obj/modtimes.pkl' in glob.glob('/home/curie/NathanCode/knoss2obj/*.pkl'):
    pkl_file = open('/home/curie/NathanCode/knoss2obj/modtimes.pkl', 'rb')
    mod_times = pickle.load(pkl_file)
    pkl_file.close()
    print('File modification times loaded from file.')
else:
    mod_times = dict()
    print('No file modification times found.')


# Determine which files to update
print('Gathering zipped raw files...')
i = 0
for root, dirnames, filenames in os.walk(dropbox_path, followlinks=True):

    for filename in fnmatch.filter(filenames, '*.zip'):

        zips.append(os.path.join(root, filename))
        current_mod_time = os.stat(os.path.join(root, filename)).st_mtime
        if filename not in mod_times.keys():
            mod_times[filename] = current_mod_time
        elif mod_times[filename] != current_mod_time:
            del mod_times[filename]
            nrrd_removal_path = nrrd_path + filename[:-5] + '.nrrd'
            obj_removal_path = obj_path + filename[:-4] + '.obj'
            os.remove(nrrd_removal_path)
            os.remove(obj_removal_path)
        i += 1

# Create a nrrd for each file for which an update is needed
for i in range(len(zips)):

    clear_raws()
    names.append(zips[i].split('/')[len(zips[i].split('/')) - 1][:-4])
    print('Converting {}...  {} of {}'.format(names[i], i + 1, len(zips)))

    current_obj_path = obj_path + names[i] + '.obj'
    current_nrrd_path = nrrd_path + '*.nrrd'
    current_nrrd_name = nrrd_path + names[i] + '.nrrd'

    if os.path.getsize(current_nrrd_name) > 1.5e10:
        print('Raw set {} is too large and will not convert to .obj with the current memory restriction.'.format(i+1))
        continue

    if current_obj_path[:-4].strip()+'.obj' in glob.glob('/home/curie/NathanCode/knoss2obj/obj/*.obj'):
        print('Raw set {} is already up to date. Moving on...'.format(i + 1))
        continue
    current_zip = zf.ZipFile(zips[i])
    current_zip.extractall(data_path)
    success = eng.startObj(names[i])

# Save modtimes back to pickle
pkl_output = open('/home/curie/NathanCode/knoss2obj/modtimes.pkl', 'wb')
pickle.dump(mod_times, pkl_output)
pkl_output.close()
clear_raws()

import code
import fnmatch
import glob
import matlab.engine
import os
import time
import zipfile as zf

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def perform_update():
    zips = []
    dropbox_path = '/media/curie/5TB/Dropbox/WebKnossos/'
    data_path = '/home/curie/knoss2obj/data/'
    obj_path = '/home/curie/knoss2obj/obj/'
    nrrd_path = '/media/curie/5TB/Dropbox/KnossNrrds/'
    print('Starting matlab engine...')
    eng = matlab.engine.start_matlab()

    print('Gathering zipped raw files...')
    i = 0

    for root, dirnames, filenames in os.walk(dropbox_path, followlinks=True):
        for filename in fnmatch.filter(filenames, '*.zip'):
            zips.append(os.path.join(root, filename))
            current_mod_time = os.stat(os.path.join(root, filename)).st_mtime
            if filename not in mod_times.keys():
                mod_times[filename] = current_mod_time
            elif mod_times[filename] != current_mod_time:
                mod_times[filename] = current_mod_time
                nrrd_removal_path = nrrd_path + filename[:-4] + '.nrrd'
                obj_removal_path = obj_path + filename[:-4] + '.obj'
                os.remove(nrrd_removal_path)
                os.remove(obj_removal_path)
            i += 1

    names = []
    for i in range(len(zips)):
        raws_to_delete = glob.glob('data/*.raw')
        for raw in raws_to_delete:
            os.remove(raw)
        names.append(zips[i].split('/')[len(zips[i].split('/')) - 1][:-4])
        print('Converting {}...  {} of {}'.format(names[i], i + 1, len(zips)))

        current_obj_name = 'obj/' + names[i] + '.obj'
        current_nrrd_path = nrrd_path + '*.nrrd'
        current_nrrd_name = nrrd_path + names[i] + '.nrrd'

        if current_obj_name in glob.glob('obj/*.obj') and current_nrrd_name in glob.glob(current_nrrd_path):
            print('Raw set {} is already up to date.'.format(i + 1))
            continue
        current_zip = zf.ZipFile(zips[i])
        current_zip.extractall(data_path)
        success = eng.start(names[i])
        print(success)


class UpdateHandler(FileSystemEventHandler):

    def on_modified(self, event):
        perform_update()

    def on_created(self, event):
        perform_update()

mod_times = dict()
perform_update()
event_handler = UpdateHandler()
observer = Observer()
observer.schedule(event_handler, path='/media/curie/5TB/Dropbox/WebKnossos/', recursive=True)
observer.start()

try:
    while True:
        time.sleep(30)
        print('I\'m watching')
except KeyboardInterrupt:
    observer.stop()
observer.join()
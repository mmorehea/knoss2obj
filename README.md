# knoss2obj
A cron job is set to run on `curie` once every 60 seconds. This job calls the python script `knossNrrdCheck.py` included in this repository. This script checks for new volumetric tracing data in the WebKnossos folder of Dropbox and converts them to `.nrrd` files before dumping them back into the Dropbox, this time in the KnossNrrds folder.

A separate cron job is set on `curie` to run once per night at 4am. This cron job performs a similar process, but checks for the need to make new `.obj` files, which are stored locally on `curie` in the obj folder of this repository. These files are never pushed to git because of their size.

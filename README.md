# knoss2obj
A cron job is set to run on `curie` once every 60 seconds. This job calls the python script `knossCheck.py` included in this repository.

When the script is called, a check will be performed to determine whether any changes or additions have been made in terms of `.zip` files in the `WebKnossos` directory of `Dropbox`.  If a new `.zip` is detected, or if one is found to have been modified since the last check, a new `.nrrd` and `.obj` file is created for it.

The resulting `.nrrd` files are kept in the `KnossNrrds` directory of `Dropbox`.

The resulting `.obj` files are kept locally on `curie` in the `obj` directory of this repository. These files are never pushed to GitHub because of their size.


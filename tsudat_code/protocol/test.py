"""
Example of using a python enum.
"""

import os


# these values should be in a global config somewhere
FtpBasePath = '/home/server/ftp_base_path'

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

Proto = Enum(('NFS', 'FTP', 'HTTP'))

DataDirectory = '/data'

ServerIP = '127.0.0.1'	# one way, could also use DNS name


def make_zip_filename(id):
    """Make unique zip file name that includes task ID."""

    return "data_%06d.zip" % id		# or use date+time

def make_zip(src, dst):
    """Zip directory 'src' to zip file 'dst'."""

    print("zipping '%s' to '%s'" % (src, dst))

def proto_tuple(task, proto, data_path):
    """Generate protocol tuple and perhaps process data files.

    task       reference to the task object
    proto      the protocol to use
    data_path  absolute path to data file *directory*
    """

    if proto == Proto.NFS:
        # nothing to do if NFS
        # if required by local sharing, pervert name to something client can use
        result = data_path
    elif proto == Proto.FTP:
        # if FTP, make zip file, return path to zip
        zip_filename = make_zip_filename(task.id)
        zip_path = os.path.join(FtpBasePath, zip_filename)
        make_zip(data_path, zip_path)
        result = 'ftp://' + ServerIP + zip_path		# make the URL
    elif proto == Proto.HTTP:
        # if HTTP, same as for FTP
        zip_filename = make_zip_filename(task.id)
        zip_path = os.path.join(FtpBasePath, zip_filename)
        make_zip(data_path, zip_path)
        result = 'http://' + ServerIP + zip_path	# make the URL
#    elif proto == Proto.????:
#        ....
#        result = ....

    return (proto, result)

# fake a task object (just .id)
class Task(object):
    pass
task = Task()
task.id = 123		# the unique task ID

# this is where we would create the data directory
task_data_path = os.path.join(DataDirectory, '%06d' % task.id)

# get proto tuple for each protocol
for p in Proto:
    (proto, detail) = proto_tuple(task, p, task_data_path)
    print('proto=%s, detail=%s' % (proto, str(detail)))

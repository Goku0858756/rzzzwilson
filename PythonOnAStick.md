# Introduction #

Sometimes we would like to be able to run software without having
to get the software installed on a Windows computer.  One approach
is to put the required software onto a USB drive and execute it
from there.  How do we do this with a python application?

This document describes one approach and shows how a wxPython
application can be run from a USB drive without installing any
software on the host computer.  It also shows how to access and
update a data file on the drive which can be a problem as the
drive letter assigned to a USB drive is not known beforehand.

The basic idea is to place a complete python installation on the
USB drive, including any extra modules.  To run the python
application we require the user to execute a BAT file in the root
directory of the USB drive.  This BAT file sets up the required
environment variables before running the application.

We create everything destined for the USB drive in a staging
directory called _usb\_image_.  This is just for convenience and
speed: compiling all `*`.py files to `*`.pyc is slow on a USB drive.

## Installing Python ##

We install a 32bit python.  This should run on a 32bit or 64bit
Windows machine.  The procedure here was performed after a clean
install of Windows 7.  It may be possible to use an existing python
installation without doing a clean install, though this will probably
include modules you don't need on the USB drive.  Since USB drives
are now cheap and large, this probably won't matter.  The
python installation doesn't take up more than about 200MB on the USB
drive. Your application can take up as little or as much space as it
requires.

  * Install the required python (2.7 in this case) to the host machine:
    1. Install 'just for me'
    1. Install to C:\Python27
    1. Install everything
  * Install any required modules (we need wxPython)
  * Copy the C:\Python27 directory to the usb\_image directory
  * Compile all `*`.py to `*`.pyc in the image directory:
```
C:\Python27\Lib\compileall.py usb_image\Python27
```
  * Remove all `*`.py files from usb\_image\Python27:
```
Do this with explorer by finding all *.py under usb_image\Python27 and then
deleting all found *.py files (not the *.pyc files!). Order by file type
before deleting (easier to select all *.py).
```


We remove all `*`.py files from the Python27 directory since a problem
was noticed when USB drives were moved from Windows machine to
Windows machine.  The initial execution of programs on the new machine
forced a recompilation of all `*`.py files used.  This slowed down
execution markedly.  The solution was to force a compile of all `*`.py
files under Python27 and then remove all `*`.py files.  Ensuring that
all `*`.pyc files have been generated in the python runtime _and_ your
application also means your application could run from a CD/DVD.

UPDATE: The **no `*`.py files means you can run from CD** thing above probably isn't true.  It seems Python is smart enough to recognize that the local directory is read-only and compiles into memory every time and doesn't create `*`.pyc files.

## Writing and installing the application ##

The application code is written in the normal way.

One problem that may arise when running on the USB drive is that we
don't know the drive letter assigned to the USB drive.  One solution
is to not refer to any files in a way that requires a drive letter.

If your application needs to access a file that is in a known place on
the drive then access the file with an absolute path from the root of
the drive.  For example, in _simple-app_ we place the _about.txt_ file
in the root of the stick and we access it with the path `/about.txt`.

Alternatively, we could use a relative path if we arrange for the RUN.bat
file (see below) to CD to the application directory.  In that case, we
could refer to the _about.txt_ file with the path `../about.txt`.

Your application won't care what the drive letter assigned to the stick
was if you have the user browse for any required file.

If all the above won't work for you, you can always get the drive letter
from the sys.argv[0](0.md) parameter and construct paths that way.

## Setting up the BAT file and application ##

We place a BAT file in the root directory of the USB drive.  This file
sets up the environment needed to run our simple application.  The file
contains:
```
set PYTHON=%CD%Python27
set PATH=%PYTHON%;%PYTHON%\DLLs;%PATH%
cd simple-app
%PYTHON%\python.exe simple-app.py
cd C:\
```

This little file sets up the PATH environment variable, CDs to the application
directory and runs the application.

The `cd C:\` is there just to ensure we don't lock the USB drive and are
unable to remove it when we are finished with it.  Note that this doesn't
always work: Windows is notorious for not allowing a USB drive to be safely
removed.

Note that we don't compile all `*`.py files to `*`.pyc and then delete the
`*`.py in the _application_.  It doesn't cause a noticeable recompilation
problem when moving to another machine.

It isn't absolutely necessary to force a compile of all `*`.py files.  If you
wait long enough the initial execution of your application _will_ succeed!

## Copy everything to the memory stick ##

Once you have done all that, copy everything in the _usb\_image_ directory to
the USB drive.

It's neater if you format the USB drive first to remove any bloatware
that the drive vendor may have added.  You can give the drive a label of
your choice.  You may format with FAT32 or NTFS.  Note that the FAT32 filesystem
has a maximum file size of 4GB.

## Miscellaneous ##

If you wish, you could place an _autorun.inf_ file and icon file into the
root directory of the USB drive.  A sample _autorun.inf_ file is:
```
[autorun]
icon=SimpleApp.ico
label=SimpleApp
shellexecute=RUN.bat
action=Run SimpleApp
```

This won't autorun in Windows 7 but will show a dialog allowing you to
open Explorer on the stick.

## Testing ##

You will test your new USB drive, of course.

You _must_ test on a Windows installation that doesn't have python installed!

The usual problems you run into at this stage are:
  * Missing DLLs
  * Missing application modules
  * Missing python modules

The missing DLL problem is usually caused by the method used to compile the
python installation on Windows.  Take note of the DLL that is missing, find
it on the C: drive of the source machine and copy it to the `usb_image\Python27`
directory.  Copy everything to the USB drive again.

The other two problems are fixed either by installing missing python modules
or adding the missing application modules.  Copy everything to the USB drive again.

Don't forget to recompile all `*`.py to `*`.pyc and remove the no longer required
`*`.py files after installing any new python modules.
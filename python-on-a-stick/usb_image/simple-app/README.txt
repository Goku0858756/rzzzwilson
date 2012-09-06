The program here is the example application for python_on_a_stick.

It uses wxPython which forces the installation of the library into
the Python on the stick.

It also accesses and changes a file outside the application
directory.  This can be a problem as the drive letter assigned to
a memory stick is not predictable.

This application will not work on Linux due to the hack used to get
around the problem of the unpredictable drive letter on a memory
stick.  One solution is to execute different code on a 'posix'
platform'.

# Introduction #


I wrote a desktop application called `eloss-flood` in wxPython for Geoscience
Australia (GA, http://www.ga.gov.au).  GA have said that they will publish `eloss-flood` as open source [RSN](http://catb.org/jargon/html/R/Real-Soon-Now.html), so I can't point you at the source code.

Anyway, the kernel of the application was a graph showing multiple linear
piece-wise continuous curves with zero or more vertical markers.  The obvious and
user-friendly approach was to allow the use to interact with the curves and
markers with the mouse.  That is, the user could hover the mouse over the
vertical markers, get a handle showing and then drag the marker line to the left
or right.  Similarly, hovering the mouse over a point on a curve would display a
handle that the user could drag thereby changing the graph.  There was also a
mid-line hotspot that the user could drag which would add a new point to the
curve.  Right-click menus allowed the user to delete curve points, etc.

That was all written as a wxPython widget, making it slightly easier to
integrate the graph into a wxPython application by hiding some of the internal
complexities that the application overall doesn't need to know.

`eloss-flood` was designed to run from a USB memory stick without requiring that
the application be installed on a Windows computer.  The method for doing that
is documented elsewhere ([PythonOnAStick](PythonOnAStick.md)).

Then the thought occurred to me: could this graph idea be run in a browser?

This approach appeals to me as we don't need to fiddle with memory sticks
which, while cheap, aren't cheap enough.  In addition, the USB approach only
works for Windows, and who wants that!  Running from a memory stick was also
a little slow to get started.  A browser approach might be faster and would work for any
operating system, but does mean that we have to dip into the morass of cross-browser
compatability.

The code here shows my experiments trying to implement the `eloss-flood` graph
widget in a browser.

Note that for simplicity everything is in one file.  This and my limited
knowledge of javascript means that what you see here isn't production code.
I hope this will improve with time!

## Requirements ##

Note that we are using HTML 5 stuff here (the `CANVAS` object) and the code may
not work in some browsers.  I test on recent Firefox releases (currently 10.0.2)
and it works fine there.  I know that it doesn't work in IE8.

It's written in javascript, so that has to be enabled in the browser.

## Running the graph ##

Load the file `graph.html` to a filesystem of your choice and point your
web browser at it.

In firefox that's a right-click on the source browse link for `graph.html`
and choose **Save Link As...**.

Or view the contents of the `graph.html` file and select **View raw file** in the details sidebar.

## Things TODO ##

Have yet to add the hotspot marker to the reference curves but that should be no problem.

I've added right-click menu handling, but I'm having problems linking a menuitem selection to a javascript function.

Since we can't write to the local filesystem from javascript, need to solve
the problem of how to save data.  This will probably require a complete
webserver solution with data sent from local javascript to the server, saved
there and sent back to the user on request.  This data will not be stored
permanently on the server.  Also look at local storage.

If we get to something usable, bundle it up as a widget and try to use it with
`pyjamas` (http://pyjs.org) if the recent (May, 2012) hijack kerfuffle doesn't kill the project!
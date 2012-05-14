#!/usr/bin/env python

"""
A program to solve the Google "Center Of Mass" puzzle.

Usage:  cofm.py <datafile>
"""


import math
import log
log = log.Log('cofm.log', log.Log.DEBUG)


MaxCoord = 5000
MinCoord = -5000

InfiniteTime = 1000000000000000000.0


def solve_puzzle(data):
    """Solve the puzzle.

    data  is an iterable of iterables.  each top-level item is
          data for one firefly: (x, y, z, vx, vy, vz)

    Returns the 'minimum distance' from (0, 0, 0) and time that happens.
    """

    log('-' * 80)
    log('data=%s' % str(data))

    # get number of fireflies
    ff_number = len(data)

    # calculate cofm position (cx0, cy0, cz0) at time 0
    # and cofm velocity (cvx0, cvy0, cvz0) at time 0
    cx0 = sum([x for (x,_,_,_,_,_) in data]) / ff_number
    cy0 = sum([y for (_,y,_,_,_,_) in data]) / ff_number
    cz0 = sum([z for (_,_,z,_,_,_) in data]) / ff_number
    cvx0 = sum([vx for (_,_,_,vx,_,_) in data]) / ff_number
    cvy0 = sum([vy for (_,_,_,_,vy,_) in data]) / ff_number
    cvz0 = sum([vz for (_,_,_,_,_,vz) in data]) / ff_number
    log('cx0=%f, cy0=%f, cz0=%f' % (cx0, cy0, cz0))
    log('cvx0=%f, cvy0=%f, cvz0=%f' % (cvx0, cvy0, cvz0))

    # now calculate time at which cofm hits a boundary
    if cvx0 == 0.0 and cvy0 == 0.0 and cvz0 == 0.0:
        boundary_time = 0.0
    else:
        try:
            if cvx0 < 0:
                time_x = (MinCoord - cx0) / cvx0
            else:
                time_x = (MaxCoord - cx0) / cvx0
        except ZeroDivisionError:
            log('setting time_x=%f' % InfiniteTime)
            time_x = InfiniteTime
    
        try:
            if cvy0 < 0:
                time_y = (MinCoord - cy0) / cvy0
            else:
                time_y = (MaxCoord - cy0) / cvy0
        except ZeroDivisionError:
            log('setting time_y=%f' % InfiniteTime)
            time_y = InfiniteTime
    
        try:
            if cvz0 < 0:
                time_z = (MinCoord - cz0) / cvz0
            else:
                time_z = (MaxCoord - cz0) / cvz0
        except ZeroDivisionError:
            log('setting time_z=%f' % InfiniteTime)
            time_z = InfiniteTime
    
        boundary_time = min(time_x, time_y, time_z)
    log('boundary_time=%f' % boundary_time)

    # get coords of this boundary point
    cxb = cx0 + cvx0*boundary_time
    cyb = cy0 + cvy0*boundary_time
    czb = cz0 + cvz0*boundary_time
    log('cxb=%f, cyb=%f, czb=%f' % (cxb, cyb, czb))

    # now we have a line segment (cx0, cy0, cz0) to (cxb, cyb, czb)
    # rewrite cofm position as paremetric in time t and calculate 
    # t for closest approach to (0,0,0)
    #
    # From Wolfram, the time of closest approach is:
    #     t = -((x1-x0).(x2-x1))/square(|x2-x1|)
    # 
    # here: x1 is c0
    #       x2 is cb
    #       x0 is the origin (0,0,0)
    # 
    # calculate sub-expressions
    if boundary_time == 0.0:
        cxc = cx0
        cyc = cy0
        czc = cz0
        closest_time = 0.0
    else:
        x1_x0_x = cx0
        x1_x0_y = cy0
        x1_x0_z = cz0
        x2_x1_x = cxb - cx0
        x2_x1_y = cyb - cy0
        x2_x1_z = czb - cz0
        dot = x1_x0_x*x2_x1_x + x1_x0_y*x2_x1_y + x1_x0_z*x2_x1_z
        sub = x2_x1_x**2 + x2_x1_y**2 + x2_x1_z**2
        closest_time = boundary_time * (-dot/sub)
        log('closest_time=%f' % closest_time)
    
        # now figure out position at closest time and get distance to origin
        cxc = cx0 + cvx0*closest_time
        cyc = cy0 + cvy0*closest_time
        czc = cz0 + cvz0*closest_time

    log('cxc=%f, cyc=%f, czc=%f' % (cxc, cyc, czc))
    min_distance = math.sqrt(cxc**2 + cyc**2 + czc**2)

    return (min_distance, closest_time)

def read_data(fd):
    """Read a set of problem data from 'fd'.

    Returns an iterable of iterables:
        ((p1x, p1y, p1z, v1x, v1y, v1z),
         (...)
         ...)
    """

    num_ff = int(fd.readline().strip())
    result = []
    for _ in xrange(num_ff):
        line = fd.readline().strip()
        line = line.split(' ')
        line_values = []
        for v in line:
            line_values.append(float(v))
        result.append(line_values)

    return result
        
def main(N, fd):
    """Solve the puzzle.

    N   is the number of datasets
    fd  is the open file to read datasets from
    """

    # solve each test case
    for case in xrange(N):
        data = read_data(fd)
        (min_distance, at_time) = solve_puzzle(data)
        print('Case #%d: %.8f %.8f' % (case+1, min_distance, at_time))

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print __doc__
        sys.exit(10)

    buildings = []
    fd = open(sys.argv[1], 'r')
    N = int(fd.readline())

    main(N, fd)

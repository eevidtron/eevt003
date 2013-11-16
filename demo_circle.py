#!/usr/bin/python
#
# eevidtron example code (youtube.com/eevidtron)
# written by Clifford Wolf (www.clifford.at)
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# boilerplate code
from __future__ import division
from __future__ import print_function

# used standard libraries
from pylab import *

# import the dcmesh module
from dcmesh import dcmesh


###############################################
# Set up and solve problem

figure()
show(block = False)

result_currents = []

for angle in range(0, 91, 9):

    print('Solving for angle=%d.' % angle)

    # create new solver object
    solver = dcmesh(300, 300)
    solver.INDENT = '  '

    # create a conductive circle
    if False:
        for y in range(solver.DIM_H):
            for x in range(solver.DIM_W):
                if (0.5+y-solver.DIM_H/2)**2 + (0.5+x-solver.DIM_W/2)**2 < (min(solver.DIM_H, solver.DIM_W)/2-0.5)**2:
                    solver.G_MAP[y, x] = 1.0

    # create a conductive trace
    if True:
        dy = sin(angle*pi/180)
        dx = cos(angle*pi/180)
        for y in range(solver.DIM_H):
            for x in range(solver.DIM_W):
                vy = y - solver.DIM_H/2;
                vx = x - solver.DIM_W/2;
                d = abs((vx*dx) + (vy*dy))
                if d < min(solver.DIM_H, solver.DIM_W)/10:
                    if (0.5+y-solver.DIM_H/2)**2 + (0.5+x-solver.DIM_W/2)**2 < (min(solver.DIM_H, solver.DIM_W)*0.4-0.5)**2:
                        solver.G_MAP[y, x] = 1.0

    # create voltage source
    r = int(min(solver.DIM_H, solver.DIM_W)/30)
    y = min(solver.DIM_H, solver.DIM_W)/4 * sin((180-angle)*pi/180)
    x = min(solver.DIM_H, solver.DIM_W)/4 * cos((180-angle)*pi/180)
    for u, center_y, center_x in [
            (1.0, int(solver.DIM_H/2 - y + 0.5), int(solver.DIM_W/2 - x + 0.5)),
            (0.0, int(solver.DIM_H/2 + y + 0.5), int(solver.DIM_W/2 + x + 0.5)) ]:
        for offset_y in range(-r, r+1):
            for offset_x in range(-r, r+1):
                if offset_x**2 + offset_y**2 < r**2:
                    solver.U_MAP[offset_x + center_x, offset_y + center_y] = u

    # run solver
    solver.solve()
    result_currents.append(solver.TOTAL_I)

    # display results
    print(solver.INDENT + 'Input current: %f' % solver.TOTAL_I)
    solver.plot()
    draw()

figure()
plot(range(0, 91, 9), result_currents)
title('Current as function of rotation angle')
ylim(0, max(result_currents)*1.2)
show(block = True)


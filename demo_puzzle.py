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

# create new solver object
solver = dcmesh(200, 200)

# create the shape
for y in range(solver.DIM_H):
    for x in range(solver.DIM_W):
        if 40 > x or x >= 160 or 80 > y or y >= 120:
            solver.G_MAP[y, x] = 2900

# create voltage source
for u, center_y, center_x in [(0.0, 160, 40), (1.0, 40, 160)]:
    for offset_y in range(-2, +3):
        for offset_x in range(-2, +3):
            solver.U_MAP[offset_y + center_y, offset_x + center_x] = u

# run solver
solver.solve()

# calculate puzzle solution
I = solver.TOTAL_I
U = solver.U_MAP[40, 80] - solver.U_MAP[160, 120]
print('Solution at 100 mA: %.3f mV' % (100*U/I))

solver.plot()
plot([120, 80], [160, 40], 'ko')
xlim(0, 200)
ylim(200, 0)
show()


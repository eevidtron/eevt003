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
solver = dcmesh(3, 3)

# create the shape
for y in range(3):
    for x in range(3):
        if y != 1 or x != 1:
            solver.G_MAP[y, x] = 1.0

# create voltage source
solver.U_MAP[0, 0] = 1.0
solver.U_MAP[2, 2] = 0.0

# run solver
solver.solve()

# display results
print('Current: %.2f A' % solver.TOTAL_I)
imshow(solver.U_MAP, cmap='jet', interpolation = 'none')
colorbar()
show()


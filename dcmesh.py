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
import scipy.sparse as sparse
import scipy.sparse.linalg as spla


###############################################
# Solver class

class dcmesh:
    """
    A simple linear dc mesh solver.
    """

    def __init__(self, W=300, H=300):
        # dimensions
        self.DIM_W = W
        self.DIM_H = H

        # conductivity map
        self.G_MAP = np.zeros((self.DIM_H, self.DIM_W))

        # voltage source map
        self.U_MAP = np.zeros((self.DIM_H, self.DIM_W)) * nan

        # prefix/indent for verbose output
        self.INDENT = ''

    def coord_to_idx(self, y, x):
        return y * self.DIM_W + x

    def is_valid_coord(self, y, x):
        if y < 0 or x < 0:
            return False
        if self.DIM_H <= y:
            return False
        if self.DIM_W <= x:
            return False
        return True

    def solve(self):
        print(self.INDENT + 'Creating equations (csr).')
        A_counter = 0
        A_data = np.zeros(self.DIM_H*self.DIM_W*5)
        A_indices = np.zeros(self.DIM_H*self.DIM_W*5, dtype=np.int)
        A_indptr = np.zeros(self.DIM_H*self.DIM_W+1, dtype=np.int)
        B = np.asmatrix(np.zeros((self.DIM_H*self.DIM_W, 1)))
        for y in range(self.DIM_H):
            for x in range(self.DIM_W):
                row = self.coord_to_idx(y, x)
                A_indptr[row] = A_counter
                col_idx = [-1,] * 5
                for col_y, col_x, k in [(y-1, x, 0), (y, x-1, 1), (y, x, 2), (y, x+1, 3), (y+1, x, 4)]:
                    if self.is_valid_coord(col_y, col_x):
                        A_indices[A_counter] = self.coord_to_idx(col_y, col_x)
                        col_idx[k] = A_counter
                        A_counter += 1
                if not isnan(self.U_MAP[y, x]):
                    A_data[col_idx[2]] = 1
                    B[row] = self.U_MAP[y, x]
                else:
                    found_valid_neigh = False
                    for neigh_y, neigh_x, k in [(y-1, x, 0), (y, x-1, 1), (y, x+1, 3), (y+1, x, 4)]:
                        if self.is_valid_coord(neigh_y, neigh_x):
                            g1 = self.G_MAP[y, x]
                            g2 = self.G_MAP[neigh_y, neigh_x]
                            if g1 != 0 and g2 != 0:
                                g = 2 * g1 * g2 / (g1 + g2)
                                A_data[col_idx[2]] += g
                                A_data[col_idx[k]] -= g
                                found_valid_neigh = True
                    if not found_valid_neigh:
                        A_data[col_idx[2]] = 1
        A_indptr[self.DIM_H*self.DIM_W] = A_counter

        print(self.INDENT + 'Solving linear system.')
        A = sparse.csr_matrix((A_data, A_indices, A_indptr), shape=(self.DIM_H*self.DIM_W, self.DIM_H*self.DIM_W))
        U = spla.spsolve(A, B)

        print(self.INDENT + 'Summing input current.')
        self.TOTAL_I = 0
        for y in range(self.DIM_H):
            for x in range(self.DIM_W):
                idx = self.coord_to_idx(y, x)
                if not isnan(self.U_MAP[y, x]) and self.U_MAP[y, x] > 0.5:
                    for neigh_y, neigh_x in [(y-1, x), (y, x-1), (y, x+1), (y+1, x)]:
                        if self.is_valid_coord(neigh_y, neigh_x):
                            neigh_idx = self.coord_to_idx(neigh_y, neigh_x)
                            g = (self.G_MAP[y, x] + self.G_MAP[neigh_y, neigh_x]) / 2
                            self.TOTAL_I += g * (U[idx] - U[neigh_idx])

        print(self.INDENT + 'Creating potential map.')
        for y in range(self.DIM_H):
            for x in range(self.DIM_W):
                if self.G_MAP[y, x] != 0:
                    idx = self.coord_to_idx(y, x)
                    self.U_MAP[y, x] = U[idx]

    def plot(self):
        clf()
        imshow(self.U_MAP, cmap='prism')
        colorbar()



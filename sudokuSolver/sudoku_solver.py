# -*- coding: utf-8 -*-
"""
sudoku_solver.py

A sudoku solving script that uses the backtracking algorithm
to brute force a solution on a sudoku puzzle

Solves a sample puzzle and unit tests functions along the way

"""

import numpy as np

print('sudoku solver script')
print(f'------------------------------------')
grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]
grid = np.matrix(grid)
print('sample sudoku grid!')
print(grid)
grid_shape = grid.shape
print(f'size of board {grid_shape}')
print(f'------------------------------------')
# access an entry
grid[0,1]

# possibleEntry function.
# user inputs the grid, (x,y)coordinate and an entry n
# function will determine whether n is a possible entry
# in the grid

def possibleEntry(grid,y,x,n):
  # check the row
  for i in range(0,9):
    if grid[y,i] == n:
      return False
  # check the column
  for i in range(0,9):
    if grid[i,x] == n: 
      return False

  ## check the box itself
  # determine the box position
  box_x = (x//3)*3
  box_y = (y//3)*3

  for i in range(0,3):
    for j in range(0,3):
      if grid[box_y + i,box_x + j] == n:
        return False
        
  return True

print(f'UNIT TESTING POSSIBLE ENTRY FUNCTION')
# unit test the possibleEntry function
x = 4
y = 4
n = 3
check = possibleEntry(grid,y,x,n) # enters an impossible entry
print(f'entering {n} at ({y},{x})...')
print(f'Test 1: {check}')

# unit test the possibleEntry function
x = 4
y = 4
n = 5
check = possibleEntry(grid,y,x,n) # enters an impossible entry
print(f'entering {n} at ({y},{x})...')
print(f'Test 2: {check}')
# find_empty
# iteratively checks the grid for empty spots in sudoku grid

def find_empty(grid):
  grid_size = grid.shape
  for i in range(grid_size[0]):
    for j in range(grid_size[1]):
      if grid[i,j] == 0:
        return (i,j) # row and col
  return None

print(f'------------------------------------')
print(f'UNIT TESTING FIND EMPTY FUNCTION')
# unit test the possibleEntry function
print(f'first possible empty spot: {find_empty(grid)}')
print(f'------------------------------------')
# solve function.
# user inputs the grid, function recursively solves
# for all possible entries until a solution is found 

def solveV2(grid):
  # check rows and cols
  find = find_empty(grid)
  if not find:
    return True # we have found the solution
  else:
    row,col = find

  for i in range(1,10):

    if possibleEntry(grid,row,col,i):
      grid[row,col] = i
      if solveV2(grid):
        return True
      grid[row,col] = 0

  return False

# test the solve function
print('input:')
print(grid)
print('')
print('output:')
solveV2(grid)
print(grid)
print(f'------------------------------------')
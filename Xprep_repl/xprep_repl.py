# A cheap version of Xprep to parse .HKL files

##################
import numpy as np
import re
import os
from matplotlib import pyplot as plt
from UC_Vol_Calculator import *
import sys
# import pymatgen.symmetry.analyzer as psa
# import gemmi as gm
# import spglib

from pyxtal.symmetry import Group
from pyxtal.symmetry import Wyckoff_position as wp
#################


#####################################################
#####################################################
# Testing pyxtal.symmetry Module:

g = Group(191)

sym_Ops=g.Wyckoff_positions[0]

sym_Ops2 = wp.from_group_and_index(191, 0)

# print(sym_Ops2)

sym_Ops3 = wp.from_symops(ops=sym_Ops2,group=191)

# print(sym_Ops3)

#####################################################
#####################################################

###################
# Read in data file
###################

#file_location = str(input('Full path to .HKL file: '))


######
# Parse header with regular expression
######

# directory_in_str = str(input('Input directory file path: '))

directory_in_str = '/Volumes/SSD_Alpha/Research/Analysis/Code/SMX_Pipeline/Xprep_repl'
#directory = os.fsencode(directory_in_str)

directory = directory_in_str 

data_diction={}   
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".HKL"):
     	print('--> Reading in file: ',os.path.join(directory, filename))
     	data_diction['%s'%str(filename)]=[]
     	data_diction['%s_headerData'%str(filename)]=[]
     	with open(filename, "r") as f:
     		for line in f:
     			line=line.strip()
     			# print(line)
     			data_diction['%s'%str(filename)].append(line)
     			if line.startswith('!'):
     				# print(line)
     				data_diction['%s_headerData'%str(filename)].append(line)
     				x=str(data_diction['%s_headerData'%str(filename)])


###########################################
# Find Unit cell Parameters
###########################################

pattern_UnitCell = re.compile(r'(!UNIT_CELL_CONSTANTS=)(\s)+([0-9]+\.[0-9]+)(\s)+([0-9]+\.[0-9]+)(\s)+([0-9]+\.[0-9]+)(\s)+([0-9]+\.[0-9]+)(\s)+([0-9]+\.[0-9]+)(\s)+([0-9]+\.[0-9]+)') 

matches_UnitCell = pattern_UnitCell.finditer(x) 

for match in matches_UnitCell:
	d1=str(match.group(3))
	d2=str(match.group(5))
	d3=str(match.group(7))
	alpha=str(match.group(9))
	beta=str(match.group(11))
	gamma=str(match.group(13))
	s2=(str(match.group(3)) + ' ' + str(match.group(5)) + ' ' + str(match.group(7)) + ' ' + str(match.group(9)) + ' ' + str(match.group(11)) + ' ' + str(match.group(13)))

# print(d1)
###########################################
# Find Energy
###########################################


pattern_WaveLength = re.compile(r'(X-RAY_WAVELENGTH=)(\s)+([a-zA-Z0-9-]\.[0-9]+)')
matches_Wavelength = pattern_WaveLength.finditer(x) 

for match in matches_Wavelength:
	# print(match.group(1))
	# print(match.group(3))
	s1=(str(match.group(3)))

###########################################
# TITL Name
###########################################

# pattern_TITL = re.compile(r'(INPUT_FILE=)([a-zA-Z0-9.-_]+_[a-zA-Z]+_[a-zA-Z]+_[0-9]+_[0-9]+)')
pattern_TITL = re.compile(r'(INPUT_FILE=)([a-zA-Z0-9.-_]+)')
matches_TITL = pattern_TITL.finditer(x) 

for match in matches_TITL:
	# print(match.group(1))
	# print(match.group(2))
	TITL_name=(str(match.group(2)))


###########################################
# Space Group #
###########################################

pattern_TITL = re.compile(r'(!SPACE_GROUP_NUMBER=)(\s)+([0-9]+)')
matches_TITL = pattern_TITL.finditer(x) 

for match in matches_TITL:
	# print(match.group(1))
	# print(match.group(3))
	space_Group_Number=(str(match.group(3)))


space_Group_diction = {
	'16': 'P222',
	'191': 'P6/mmm'
}


symmetry_op_diction = {
	'16': 'SYMM +X -Y 1/2-Z\nSYMM -X +Y -Z\nSYMM -X -Y 1/2+Z',
	'191': 'SYMM -Y, X-Y, +Z\nSYMM Y-X, -X, +Z\nSYMM -X, -Y, +Z\nSYMM +Y, Y-X, +Z\nSYMM X-Y, +X, +Z\nSYMM +Y, +X, -Z\nSYMM X-Y, -Y, -Z\nSYMM -X, Y-X, -Z\nSYMM -Y, -X, -Z\nSYMM Y-X, +Y, -Z\nSYMM +X, X-Y, -Z'
}



#####################################################
#####################################################
# Calculating Unit Cell Volume

sg_symbol = space_Group_diction[str(space_Group_Number)]

# print('TEST', d1,d2,d3)

noAtoms_ASU = int(input('How many atoms are in the ASU? '))
# noAtoms_ASU = 129
SFAC = input("Input SFAC: ")
UNIT = input('Input UNIT: ')
# TREF = input('Input TREF: ')

CellCalcs = unitCell_Calcs(spacegroupSymbol=str(sg_symbol),a=float(d1),b=float(d2),c=float(d3),alpha=float(alpha),beta=float(beta),gamma=float(gamma),no_atoms_ASU=noAtoms_ASU)

z = CellCalcs.calc_Z()


#####################################################
#####################################################
# L1='TITL', TITL_name, 'in', '%s'%str(space_Group_diction[str(space_Group_Number)]), '#%s'%str(space_Group_Number)
# f = open('cXPREP.ins','w')
# f.write(str(L1))

orig_stdout = sys.stdout
f = open('cXPREP.ins', 'w')
sys.stdout = f

print('TITL', TITL_name, 'in', '%s'%str(space_Group_diction[str(space_Group_Number)]), '#%s'%str(space_Group_Number))
print('REM', ' reset to', '%s'%str(space_Group_diction[str(space_Group_Number)]), '#%s'%str(space_Group_Number))
print('CELL',s1,s2)
print('ZERR', str('%s'%str(round(z,2))), '0.000', '0.000', '0.000')
print('LATT', '-1')


try:
	print(symmetry_op_diction[str(space_Group_Number)])
except KeyError:
	print('------->')
	print('We currently do not have the symmtry operators for that particular space group')
	print('The script has failed & terminated...')
	print('Contact rcm347@cornell.edu such that the issue can be address!')
	print('<-------')
	exit()


## User Inputs ##

# SFAC = input("Input SFAC: ")
# UNIT = input('Input UNIT: ')
# TREF = input('Input TREF: ')

print('SFAC', SFAC)
print('UNIT', UNIT)
print('TREF')
print('\nHKLF', str('%s'%str(round(z,2))))
print('END')

sys.stdout = orig_stdout
f.close()




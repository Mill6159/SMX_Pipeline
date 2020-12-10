# A cheap version of Xprep to parse .HKL files

##################
import numpy as np
import re
import os
from matplotlib import pyplot as plt
#################

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


x = str(data_diction['XSCALE.HKL_headerData'])

###########################################
# Find Unit cell Parameters
###########################################

pattern_UnitCell = re.compile(r'(!UNIT_CELL_CONSTANTS=)(\s)+([a-zA-Z0-9-]\.[0-9]+)(\s)+([0-9]+\.[0-9]+)(\s)+([0-9]+\.[0-9]+)(\s)+([0-9]+\.[0-9]+)(\s)+([0-9]+\.[0-9]+)(\s)+([0-9]+\.[0-9]+)') 

matches_UnitCell = pattern_UnitCell.finditer(x) 

for match in matches_UnitCell:
	# print(match.group(3))
	# print(match.group(5)) 
	# print(match.group(7))
	# print(match.group(9))
	# print(match.group(11))
	# print(match.group(13))
	s2=(str(match.group(3)) + ' ' + str(match.group(5)) + ' ' + str(match.group(7)) + ' ' + str(match.group(9)) + ' ' + str(match.group(11)) + ' ' + str(match.group(13)))


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

pattern_TITL = re.compile(r'(INPUT_FILE=)([0-9]+_[a-zA-Z]+_[a-zA-Z]+_[0-9]+_[0-9]+)')
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


print('TITL', TITL_name, 'in', 'ENTER SPACE GROUP', '#%s'%str(space_Group_Number))
print('REM', ' reset to', 'ENTER SPACE GROUP', '#%s'%str(space_Group_Number))
print('CELL',s1,s2)
print('ZERR')
print('LATT', '-1')
print('SYMM')
print('SYMM')
print('SYMM')
print('SFAC')
print('UNIT')
print('TREF')
print('\nHKLF 4')
print('END')






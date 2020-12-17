import numpy as np

### User inputs

# No. of atoms in asymmetric unit
# Estimated No. of ASU's in the unit cell
# From that we can calculate "Z"


class unitCell_Calcs():

	def __init__(self,spacegroupSymbol='P1',a=9.89,b=10.07,c=51.94,alpha=90,beta=90,gamma=90,no_atoms_ASU=100):
		'''Initialize parameters..

		'''
		# print('---> Starting Unit Cell Calculations')
		self.spacegroupSymbol=spacegroupSymbol
		self.a = a
		self.b = b
		self.c = c
		self.alpha = alpha
		self.beta = beta
		self.gamma = gamma
		self.no_atoms_ASU = no_atoms_ASU

	def unitCell_determination(self):
		'''
		From input file the space group symbol can be extracted
		Use that to determine the unitCell type
		'''
		spacegroupSymbol=self.spacegroupSymbol
		unitCell=[]

		orthorhombic=['P222','P2221','P21212','P212121','C2221','C222','F222','I222','I212121']
		tetragonal=['P4','P41','P42','P43','I4','I41']
		hexagonal=['P6/mmm']

		if spacegroupSymbol=='P1':
			unitCell.append('triclinic')
		elif spacegroupSymbol=='P2' or spacegroupSymbol=='P21':
			unitCell.append('monoclinic')
		elif spacegroupSymbol in orthorhombic:
			unitCell.append('orthorhombic')
		elif spacegroupSymbol in tetragonal:
			unitCell.append('tetragonal')
		elif spacegroupSymbol in hexagonal:
			unitCell.append('hexagonal')

		self.unitCell=unitCell[0]

		return unitCell[0]


	def calc_UC_volume(self):
		'''
		a=
		b=
		c=
		alpha=
		beta=
		gamma=
		unitCell= # how it is calced
		'''

		## Generate conditional for each space group:
		a=self.a
		b=self.b
		c=self.c
		alpha=self.alpha
		beta=self.beta
		gamma=self.gamma
		uc_Volume=[]
		unitCell=self.unitCell_determination()

		if unitCell=='orthorhombic':
			uc_Volume.append(a*b*c)
		elif unitCell=='monoclinic':
			uc_Volume.append(a*b*c*np.sin(beta))
		elif unitCell=='trigonal':
			uc_Volume.append((a**2)*c*np.sin(60 * (np.pi/180)))
		elif unitCell=='hexagonal':
			uc_Volume.append((a**2)*c*np.sin(60 * (np.pi/180)))
		elif unitCell=='isometric':
			uc_Volume.append(a*a*a)
		elif unitCell=='tetragonal':
			uc_Volume.append(a*a*c)
		elif unitCell=='triclinic':
			uc_Volume.append((a*b*c) * (1-np.cos(alpha * (np.pi/180))-np.cos(beta * (np.pi/180))-np.cos(gamma * (np.pi/180))) + 2 *(np.cos(alpha * (np.pi/180))*np.cos(beta * (np.pi/180))*np.cos(gamma * (np.pi/180)))**(1/2))


		self.uc_Volume=uc_Volume[0]


		return uc_Volume[0]




	def calc_Z(self):
		'''
		How to calculate this...
		'''
		UC_volume = self.calc_UC_volume()
		no_atoms = self.no_atoms_ASU

		z=(UC_volume/(no_atoms * 10)) # we should round this..

		return z



# test = unitCell_Calcs(spacegroupSymbol='P222')

# x=test.unitCell_determination()
# print(x)
# y=test.calc_UC_volume()
# print(y)

# # w=test.calc_Z()
# print(w)

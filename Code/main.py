# -*- coding: utf-8 -*

import argparse
from numpy import pi
from assemblage_mat import Assemblage 
from paraview import paraview
import time


parser = argparse.ArgumentParser()
parser.add_argument("-f", required=True, type=str, help="Entrez un fichier")
parser.add_argument("-k", metavar="r", default=2*pi, type=float, help="Entrez un nombre d'onde k")
parser.add_argument("-a", metavar="r", default=pi/2, type=float, help="Entrez un alpha")



if __name__ == '__main__':
	args = parser.parse_args()

	filename = args.f
	k = args.k
	a = args.a


	debut = time.time()

	test = Assemblage(filename,k,a)
	t1 = time.time()
	print("\nTemps lecture fichier : "+str(t1-debut))

	tmp = time.time()
	test.Mass()
	t2 = time.time()
	print("\nTemps créat Matrice Masse : "+str(t2-tmp))

	tmp = time.time()
	test.Rigi()
	t3 = time.time()
	print("\nTemps creat MAtrice Rigidte: "+str(t3-tmp))

	tmp = time.time()
	test.Four_Robin()
	t4 = time.time()
	print("\nTemps creat Matrice Four_Robin : "+str(t4-tmp))

	tmp = time.time()
	test.assemb_mat()
	t5= time.time()
	print("\nTemps Assemblage: "+str(t5-tmp))

	paraview(test)

	fin = time.time()

	print("\nFin de l'algorithme : "+str(fin-debut))


# -*- coding: utf-8 -*

import argparse
from assemblage_mat import Assemblage 
from paraview import paraview
import time


parser = argparse.ArgumentParser()
parser.add_argument("-f", required=True, type=str, help="Entrez un fichier")


if __name__ == '__main__':
	args = parser.parse_args()

	filename = args.f

	debut = time.time()

	test = Assemblage(filename)
	t1 = time.time()
	print("Temps lecture fichier : "+str(t1-debut))

	tmp = time.time()
	test.Mass()
	t2 = time.time()
	print("Temps créat Matrice Masse : "+str(t2-tmp))

	tmp = time.time()
	test.Rigi()
	t3 = time.time()
	print("Temps creat MAtrice Rigidte: "+str(t3-tmp))

	tmp = time.time()
	test.Four_Robin()
	t4 = time.time()
	print("Temps creat Matrice Four_Robin : "+str(t4-tmp))

	tmp = time.time()
	test.assemb_mat()
	t5= time.time()
	print("Temps Assemblage: "+str(t5-tmp))

	paraview(test)

	fin = time.time()

	print("Fin de l'algorithme : "+str(fin-debut))


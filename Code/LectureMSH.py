# -*- coding: utf-8 -*-
"""

	Cette fonction permet de lire lun fichier .msh 


"""
import numpy as np 



def lecture_fichier(filename):

	nbr_nodes=0
	nbr_elements=0
	non_triangle = 0 
	liste_nodes = []
	liste_element = []
	with open(filename,"r") as fichier:
		while fichier.readline() != "$Nodes\n":
			pass	

		#Lecture Triangles
		nbr_nodes = int(fichier.readline())

		for i in range(nbr_nodes):

			sommet = fichier.readline().split(" ")
			liste_nodes.append((float(sommet[1]),float(sommet[2]),float(sommet[3])))


		fichier.readline()
		fichier.readline()

		#Lecture Elements
		nbr_elements=int(fichier.readline())

		for j in range(nbr_elements):
			

			element= fichier.readline().split(" ")

			# element[3] = 1 -> intérieur
			# element[3] = 2 -> ellipse
			# element[3] = 3 -> sous-marin

			if(int(element[1])==1):
				non_triangle +=1
				liste_element.append((int(element[1]),int(element[3]),int(element[5]),int(element[6])))
			elif(int(element[1])==2):
				liste_element.append((int(element[1]),int(element[3]),int(element[5]),int(element[6]),int(element[7])))

	return nbr_nodes, liste_nodes, nbr_elements, liste_element, non_triangle



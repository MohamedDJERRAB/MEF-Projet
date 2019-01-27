# MEF : Résolution du problème de diffraction d’une onde acoustique par un sous-marin
**En utilisant la méthode des éléments finis P1-Lagrange**


#Contenu du Git

Ce dépôt git est constitué de plusieurs fichier:

	- Code **->** Il contient tout les fichiers Python permettant de résoudre le problème
	- fichierGMSH **->** Il contient les fichier gmsh (.geo et .msh)
	- FreeFem **->** Il contient les fichier .edp afin de pouvoir visualiser la solution et comparer avec Paraview

#Execution des Fichiers

Lancez le fichier main.py du fichier **Code** pour calculer la modélisation de la manière suivante :
	
	python Code/main.py -f fichierGMSH/"monfichier.msh"


Pour visualiser la modélisation, grâce u code paraview.py :
	
	paraview Code/rendu_maillage.vtu
	FreeFem++ FreeFem/helmholtz.edp

**Attention !** Il faut changer le chemin du .msh dans le fichier helmholtz.edp

###############################


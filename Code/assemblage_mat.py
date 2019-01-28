# -*- coding: utf-8 -*

import numpy as np
from LectureMSH import lecture_fichier
from scipy.sparse import coo_matrix,csr_matrix,linalg

class Assemblage:
	"""docstring for ClassName"""

	def __init__(self, filename,k,a):
		assert filename, "Entrez un fichier !"
		
		self.k = k
		self.a = a
		self.nbr_nodes, self.liste_nodes, self.nbr_elements, self.liste_element,self.non_tri = lecture_fichier(filename)


	#Fonction pour passer des sommets locaux aux globaux
	def Loc2Glob(self,p,i):
		if i <= 0 and i > 3:
			raise Exception("Erreur indice sommet triangle")

		if self.liste_element[p-1][1] == 1 and i >= 3:
			raise Exception("Erreur coord segment")

		return self.liste_element[p-1][2+i] #Va renvoyer donc le sommet global du sommet local i pour le triangle p

	#Matrice de Masse
	def Mass(self):
		ligne = []
		colonne = []
		data = []

		for p in range(self.non_tri+1,self.nbr_elements+1):
			p0 = self.liste_nodes[self.Loc2Glob(p,0)-1]
			p1 = self.liste_nodes[self.Loc2Glob(p,1)-1]
			p2 = self.liste_nodes[self.Loc2Glob(p,2)-1]


			#Calcul du déterminant de la matrice Jacobienne
			djac = (p1[0] - p0[0])*(p2[1] - p0[1]) - (p2[0] - p0[0])*(p1[1] - p0[1])

			#Calcul des coefficients
			for i in range(3):
				I = self.Loc2Glob(p,i) - 1

				for j in range(3):
					J = self.Loc2Glob(p,j) - 1

					if I == J:
						data.append(djac/12.0)

					else : 
						data.append(djac/24.0)

					ligne.append(I)
					colonne.append(J)

		#Construction de la matrice Masse
		self.M = coo_matrix((-self.k*self.k*np.array(data),(ligne,colonne))).tocsr()

		#TEST
		print("\n Verification de la Matrice de M \n")
		u = np.ones((self.nbr_nodes,1))
		tmp = self.M.dot(u)
		print(sum(tmp))
		

	#Matrice de Rigidité
	def Rigi(self):

		ligne = []
		colonne = []
		data = []	

		#gradient du triangle de référence
		gradp = [np.array([[-1,-1]]), np.array([[1,0]]), np.array([[0,1]])] 

		for p in range(self.non_tri+1,self.nbr_elements+1):

			p0 = self.liste_nodes[self.Loc2Glob(p,0)-1]
			p1 = self.liste_nodes[self.Loc2Glob(p,1)-1]
			p2 = self.liste_nodes[self.Loc2Glob(p,2)-1]

			#Determinant de la Jacobienne
			djac = (p1[0] - p0[0])*(p2[1] - p0[1]) - (p2[0] - p0[0])*(p1[1] - p0[1])

			#Calcul de Bk, inverse de la Jacobienne
			Bk = 1.0/djac *  np.array([[p2[1] - p0[1], p0[1] - p1[1]],[p0[0] - p2[0], p1[0] - p0[0]]])

			Bknew = np.matmul(np.transpose(Bk),Bk)

			for i in range(3):
				I = self.Loc2Glob(p,i) - 1

				for j in range(3):
					J = self.Loc2Glob(p,j) - 1

					inte = gradp[j].dot(Bknew)
					data.append(djac/2.0 * inte.dot(np.transpose(gradp[i]))[0][0])

					ligne.append(I)
					colonne.append(J)

		self.D = coo_matrix((data,(ligne,colonne))).tocsr()

		# TEST -> 
		print("\nVérification de la matrice D\n")

		U = np.ones((self.nbr_nodes,1))
		print(sum(self.D.dot(U)))


	#Matrice pour les conditions de bords Fourier-Robin
	def Four_Robin(self):
		ligne = []
		colonne = []
		data = []

		for p in range(1,self.non_tri+1):

			if self.liste_element[p-1][1]==2:
				p0 = self.liste_nodes[self.Loc2Glob(p,0)-1]
				p1 = self.liste_nodes[self.Loc2Glob(p,1)-1]

				S = np.linalg.norm((p0[0]-p1[0],p0[1]-p1[1]))

				for i in range(2):
					I = self.Loc2Glob(p,i)-1

					for j in range(2):
						J = self.Loc2Glob(p,j)-1

						if I == J:
							data.append(np.complex(0,1)*self.k*S/3.0)

						else:
							data.append(np.complex(0,1)*self.k*S/6.0)

						ligne.append(I)
						colonne.append(J)

		self.MFR = coo_matrix((np.array(data),(ligne,colonne)),shape=(self.nbr_nodes,self.nbr_nodes),dtype=complex).tocsr()


	#Fonction u_inc
	def u_inc(self,x,y):
		return np.exp(np.complex(0,1)*self.k*(x*np.cos(self.a) + y*np.sin(self.a)))

	def assemb_mat(self):
		
		self.A = (self.M + self.D + self.MFR).tolil()
		self.b = np.zeros(self.nbr_nodes,dtype = complex)

		for index,elem in enumerate(self.liste_element):
			if elem[1] ==3:
				for i in elem[2:]:
					self.A[i-1,:]=0
					self.A[i-1,i-1]=1
					self.b[i-1] = -self.u_inc(self.liste_nodes[i-1][0],self.liste_nodes[i-1][1])

		self.A = self.A.tocsr()

		#Resolution du problème
		self.u = linalg.spsolve(self.A, self.b)

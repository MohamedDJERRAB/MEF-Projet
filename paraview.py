# -*- coding: utf-8 -*

from assemblage_mat import Assemblage

def paraview(rendu,output = "rendu_maillage.vtu"):

	with open(output,"w") as file:
		file.write('<VTKFile type="UnstructuredGrid" version="1.0" byte_order="LittleEndian" header_type="UInt64">')
		file.write('\n<UnstructuredGrid>')
		file.write('\n<Piece NumberOfPoints="' + str(rendu.nbr_nodes) + '" NumberOfCells="' + str(rendu.nbr_elements) + '">')
		file.write('\n<Points>')
		file.write('\n<DataArray NumberOfComponents="3" type="Float64">')

		for p in rendu.liste_nodes:
			file.write('\n' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]))
		
		file.write('\n</DataArray>')
		file.write('\n</Points>')
		file.write('\n<Cells>')
			
		off = 0 # valeur de offset en int
		offsets = "" # pour ne pas parcourir plusieurs fois les éléments
		types = ""

		file.write('\n<DataArray type="Int32" Name="connectivity">')
		for indice, element in enumerate(rendu.liste_element):
			file.write('\n' + " ".join(str(s-1) for s in element[2:]))
			if element[0] == 1: # segment
				types += "\n" + str(3) # 3 représente un segment pour paraview
				off += 2
			elif element[0] == 2: # triangle
				types += "\n" + str(5) # 5 représente un triangle pour paraview
				off += 3
			offsets += "\n" + str(off)

		file.write('\n</DataArray>')

		file.write('\n<DataArray type="Int32" Name="offsets">')
		file.write(offsets)
		file.write('\n</DataArray>')

		file.write('\n<DataArray type="UInt8" Name="types">')
		file.write(types)
		file.write('\n</DataArray>')
		file.write('\n</Cells>')

		file.write('\n<PointData Scalars="rendu">')

		file.write('\n<DataArray type="Float64" Name="Partie Réelle" format="ascii">')
		for reel in rendu.u.real:
			file.write('\n'+str(reel))
		file.write('\n</DataArray>')

		file.write('\n<DataArray type="Float64" Name="Partie Imaginaire" format="ascii">')
		for imag in rendu.u.imag:
			file.write('\n'+str(imag))
		
		file.write('\n</DataArray>')
		file.write('\n</PointData>\n</Piece>\n</UnstructuredGrid>\n</VTKFile>')
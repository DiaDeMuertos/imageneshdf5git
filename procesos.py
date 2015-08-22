'''
Created on 22/08/2015

@author: Topo
'''

import numpy as np
import h5py 
import os
import glob

def leerhdf5(ruta):
        
    listaDeArchivos = []
    for d in os.walk(ruta).next()[1]:
        listaDeArchivos.append(glob.glob(os.path.join(ruta,d)+r"\*.hdf5")[0])
         
    for ra in listaDeArchivos:
        nombreArchivo = os.path.basename(ra)
     
        archHDF5 = h5py.File(ra)
        matrizDatos = archHDF5["LEVEL3/NDVI/NDVI"]
        y,x = matrizDatos.shape
        lon = float(archHDF5["LEVEL3/NDVI/NDVI"].attrs["MAPPING"][3])
        lat = float(archHDF5["LEVEL3/NDVI/NDVI"].attrs["MAPPING"][4])
        saltoX = float(archHDF5["LEVEL3/NDVI/NDVI"].attrs["MAPPING"][5])
        saltoY = float(archHDF5["LEVEL3/NDVI/NDVI"].attrs["MAPPING"][6])
        cordInicial = (lon,lat)
        boundingBox = ((lon,lat),(lon+(saltoX*x),lat-saltoY*y))
        
        print lon,lat 
        gradosLon = np.arange(-120.0,-110.0,saltoX)
        gradosLat = np.arange(35,25,-saltoY)
         
        bBox = (-111.15333,29.01645+0.009775000000000016,-111.12987,29.00053-0.009775000000000016)
     
        print "Processando....."

        rLon1 = gradosLon>=bBox[0]
        rLon2 = gradosLon<=bBox[2]
         
        rLat1 = gradosLat<=bBox[1]
        rLat2 = gradosLat>=bBox[3]
         
        union = zip(list(rLon1),list(rLon2),list(rLat1),list(rLat2))
         
        xIndices = list()
        yIndices = list()
        for indice,par in enumerate(union):
            if par[0] & par[1]:
                xIndices.append(indice)
            if par[2] & par[3]:
                yIndices.append(indice)
         
        xMin = np.array(xIndices).min()
        xMax = np.array(xIndices).max() + 1
        yMin = np.array(yIndices).min()
        yMax = np.array(yIndices).max() + 1
                 
        np.savetxt(os.path.join(ruta,nombreArchivo.split(".")[0]+".csv"), matrizDatos[yMin:yMax,xMin:xMax], delimiter=",")                                       
        archHDF5.close()


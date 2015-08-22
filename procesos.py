'''
Created on 22/08/2015

@author: Topo
'''

import numpy as np
import h5py 
import os
import glob

class cordenada:
    lon = None
    lat = None
     
    def __init__(self,lon, lat):
        self.lon = lon
        self.lat = lat
        
def leerArchivoConfig():
    archivoConfiguracion = open("configuracion.txt")
    renglon1 = archivoConfiguracion.readline().split(",")
    renglon2 = archivoConfiguracion.readline().split(",")
    renglon3 = archivoConfiguracion.readline().split(",")
    
    variables={}
    variables[renglon1[0]] = cordenada(float(renglon1[1]),float(renglon1[2])+float(renglon1[3]))
    variables[renglon2[0]] = cordenada(float(renglon2[1]),float(renglon2[2])+float(renglon2[3]))
    variables[renglon3[0]] = renglon3[1].strip()
    
    archivoConfiguracion.close()
                                        
    return variables    

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
        gradosLon = np.arange(-120.0,-110.0,saltoX)
        gradosLat = np.arange(35,25,-saltoY)
        boundingBoxNuevo = ((lon,lat),(gradosLon[-1],gradosLat[-1]))
        boundingBoxOriginal = ((lon,lat),(lon+(saltoX*x),lat-saltoY*y))
         
        
         
        bBox = (-111.15333,29.01645+0.009775000000000016,-111.12987,29.00053-0.009775000000000016)
     
        print "Processando....."
        print "{0}{1}".format("Imagen:",nombreArchivo.split(".")[0])
        print "{0:<20}{1}".format("codenadas inicial:",cordInicial)
        print "{0:<20}{1}".format("BoundingBox 1:",boundingBoxOriginal)
        print "{0:<20}{1}".format("BoundingBox 2:",boundingBoxNuevo)
        print "{0:<20}{1}".format("x,y:",(len(gradosLon),len(gradosLat)))

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


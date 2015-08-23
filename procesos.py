'''
Created on 22/08/2015

@author: Topo
'''

import numpy as np
import h5py 
import os
import glob
import csv
import gdal
import osr

saltoX = None
saltoY = None

class cordenada:
    lon = None
    lat = None
     
    def __init__(self,lon, lat):
        self.lon = lon
        self.lat = lat

class boundingBox:
    cordenadaSuperior = None
    cordenadaInferior = None
    
    def __init__(self,cordenadaSuperior,cordenadaInferior):
        self.cordenadaSuperior = cordenadaSuperior
        self.cordenadaInferior = cordenadaInferior
        
def leerArchivoConfig():
    archivoConfiguracion = open("configuracion.txt")
    renglon1 = archivoConfiguracion.readline().split(",")
    renglon2 = archivoConfiguracion.readline().split(",")
    renglon3 = archivoConfiguracion.readline().split(",")
    renglon4 = archivoConfiguracion.readline().split(",")
    archivoConfiguracion.readline()
    renglon5 = archivoConfiguracion.readline().split(",")
    renglon6 = archivoConfiguracion.readline().split(",")
    renglon7 = archivoConfiguracion.readline().split(",")
    renglon8 = archivoConfiguracion.readline().split(",")
    
    
    variables={}
    variables[renglon1[0]] = cordenada(float(renglon1[1]),float(renglon1[2])+float(renglon1[3]))
    variables[renglon2[0]] = cordenada(float(renglon2[1]),float(renglon2[2])+float(renglon2[3]))
    variables[renglon3[0]] = float(renglon3[1])
    variables[renglon4[0]] = renglon4[1].strip()
    
    variables[renglon5[0]] = cordenada(float(renglon5[1]),float(renglon5[2]))
    variables[renglon6[0]] = cordenada(float(renglon6[1]),float(renglon6[2]))
    variables[renglon7[0]] = float(renglon7[1])
    variables[renglon8[0]] = renglon8[1].strip()
    
    archivoConfiguracion.close()
                                        
    return variables    

def leerhdf5(ruta,bbDeInteres,saltoGradoD):
        
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
        global saltoX,saltoY  
        saltoX = float(archHDF5["LEVEL3/NDVI/NDVI"].attrs["MAPPING"][5])
        saltoY = float(archHDF5["LEVEL3/NDVI/NDVI"].attrs["MAPPING"][6])
        
        cordInicial = (lon,lat)
        gradosLon = np.arange(lon,lon + saltoGradoD,saltoX)
        gradosLat = np.arange(lat,lat - saltoGradoD,-saltoY)
        boundingBox = ((lon,lat),(gradosLon[-1],gradosLat[-1]))
        
        bBox = (bbDeInteres.cordenadaSuperior.lon,
                bbDeInteres.cordenadaSuperior.lat,
                bbDeInteres.cordenadaInferior.lon,
                bbDeInteres.cordenadaInferior.lat)
             
        print "Processando....."
        print "{0:<20}{1}".format("Imagen:",nombreArchivo.split(".")[0])
        print "{0:<20}{1}".format("codenadas inicial:",cordInicial)
        print "{0:<20}{1},{2}".format("Salto lon y lat:",saltoX,saltoY)
        print "{0:<20}{1}".format("BoundingBox:",boundingBox)
        print "{0:<20}{1}".format("x,y:",(len(gradosLon),len(gradosLat)))
        print "{0:<20}{1}".format("Salgo grado:",saltoGradoD)
        print "{0:<20}{1}".format("Area interes",bBox)
 
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

def importartiff(ruta,bbDeInteres):
     
    listaDeArchivos = glob.glob(ruta+r"\*.csv")
    for ra in listaDeArchivos:
        nombreArchivo = os.path.basename(ra)

        reader=csv.reader(open(ra,"rb"),delimiter=',')
        x=list(reader)
        result=np.array(x).astype('float')
        grid = result
        
        output_file = os.path.join(ruta,nombreArchivo.split(".")[0]+".tif")
        
        ncols = grid.shape[1]
        nrows = grid.shape[0]       
        
        xllcorner = bbDeInteres.cordenadaSuperior.lon
        yllcorner = bbDeInteres.cordenadaSuperior.lat
        
        global saltoX,saltoY
        xCellSize = saltoX
        yCellSize = -saltoY
        
#         print grid.shape
#         print grid[0,0]
        
        driver = gdal.GetDriverByName("GTiff")
        dst_ds = driver.Create(output_file,ncols,nrows, 1, gdal.GDT_Byte )
        # raster = grid[::-1]
        raster = grid
        
        # # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
        dst_ds.SetGeoTransform([xllcorner, xCellSize, 0, yllcorner, 0, yCellSize])
          
        # set the reference info 
        srs = osr.SpatialReference()
        srs.SetWellKnownGeogCS("WGS84")
        dst_ds.SetProjection(srs.ExportToWkt())
#         print raster.shape
        
        # write the band
        dst_ds.GetRasterBand(1).WriteArray(raster)
        ary = dst_ds.GetRasterBand(1).ReadAsArray()
#         print ary[0,0]
        ds = None        
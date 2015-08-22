'''
Created on 22/08/2015

@author: Topo
'''
import os
import procesos

if __name__ == '__main__':
    print "inicio"
    
    ruta = r"datosHDF5"
    
    procesos.leerhdf5(ruta)    
    
    print "fin..................."
#     os.system("pause")
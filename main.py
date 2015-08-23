'''
Created on 22/08/2015

@author: Topo
'''
import os
import procesos
import time

if __name__ == '__main__':
    print "inicio"
    variables = procesos.leerArchivoConfig()
    
    print "precione 1 o 2 para la configuracion:" 
    print " "*5 +"1 Default"
    print " "*5 + "2 Para otra"
    
    op = raw_input("opcion:")
    print "\n"
    
    if "1" == op.strip():
        print "Opcion 1 DEFAULT inica en 5 segudos"
        print "\n"
        time.sleep(5)       
        
        bbDeInteres = procesos.boundingBox(variables["BBPuntoSuperiorIzqD"],variables["BBPuntoInferiorDerD"])        
        saltoGradoD = variables["saltoGradoD"]    
        ruta = os.path.join(os.getcwd(),variables["rutaD"])
        
        procesos.leerhdf5(ruta,bbDeInteres,saltoGradoD)
        procesos.importartiff(ruta,bbDeInteres)
        
        print "\n"
    elif "2" == op.strip():
        print "Opcion 2 OTRA inica en 5 segudos"
        print "\n"
        time.sleep(5)
        
        bbDeInteres = procesos.boundingBox(variables["BBPuntoSuperiorIzqO"],variables["BBPuntoInferiorDerO"])    
        saltoGradoD = variables["saltoGradoO"]    
        ruta = os.path.join(os.getcwd(),variables["rutaO"])
        
        procesos.leerhdf5(ruta,bbDeInteres,saltoGradoD)
        procesos.importartiff(ruta,bbDeInteres)
        
        print "\n"
    else:        
        print "no existe la opcion..."+op.strip()     
    
    print "fin..................."
    os.system("pause")
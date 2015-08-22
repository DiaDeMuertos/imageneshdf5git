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
    print " "*5 + "2 para otra"
    
    op = raw_input("opcion:")
    print "\n"
    
    if "1" == op.strip():
        print "Opcion 1 DEFAULT inica en 5 segudos"
        time.sleep(5)
        ruta = os.path.join(os.getcwd(),variables["ruta"])
        procesos.leerhdf5(ruta)
    elif "2" == op.strip():
        print "Opcion 2 OTRA inica en 5 segudos"
        time.sleep(5)
        print "CommingSOON........"
    else:        
        print "no existe la opcion..."+op.strip()     
    
    print "fin..................."
    os.system("pause")
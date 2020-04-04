
#cd D:\MP\Dev
import sys
import os 
import csv
import ramas 
import componentes

raiz = "D:\\MP\\Dev"

def main(argv):
    #lstFolder()
    varLstSoluciones = lstSoluciones("listado_soluciones.txt")
    procesar(varLstSoluciones)

 

def procesar(varLstSoluciones):
    for x in varLstSoluciones:
        slnFile = x.split(";")[1].replace("\n","") 
        nombre_proyecto = x.split(";")[0] 
        proyecto_configuracion = lstProyectos(slnFile)
        for y in proyecto_configuracion:
            ruta_proyecto = raiz +"\\"+ y.ruta_proyecto 
            if y.ruta_proyecto.endswith(".csproj"):
                escribir_csv(lstComponentes(ruta_proyecto, nombre_proyecto))
                #print(raiz +"\\"+ y.ruta_proyecto)
        


def escribir_csv(list):
    iter_list = iter(list)
    f = open("listado.csv","a")
    with f:
        for row in iter_list:
            proyecto = os.path.basename(row.solucion).replace(".csproj","") 
            f.write(row.proyecto + ";" + proyecto + ";" + row.componente + ";"  + row.version + "\n")
    f.close()


def lstComponentes(proyecto_configuracion, proyecto):
    f = open(proyecto_configuracion, "r")
    flineas = f.readlines()
    f.close()
    lstComponentesProyecto = []
    for x in flineas:
        if  "<Reference Include=" in x:
            componente = x.split(",")[0].replace('<Reference Include="',"").lstrip()
            if "Version" in x:
                version = x.split(",")[1].replace("Version=","").lstrip()
                componenteVersion = componentes.Componentes(proyecto_configuracion,proyecto,componente, version)
                lstComponentesProyecto.append(componenteVersion)
    return lstComponentesProyecto


def lstProyectos(archivo_sln):
    ruta_solucion = os.path.dirname(archivo_sln)
    lstProyectosRama = [] 
    f = open(archivo_sln, "r")

    f1 = f.readlines()
    f.close()
    for x in f1:
        if x.startswith("Project") == True:
            nombre_proj = x.split("=")[1]
            
            modulo = nombre_proj.split(",")[0]
            proyecto = nombre_proj.split(",")[1].replace('"','').lstrip()
            ruta_proyecto = ruta_solucion + "\\" + proyecto

            rama = ramas.Ramas(ruta_solucion, modulo, ruta_proyecto,proyecto)
            lstProyectosRama.append(rama)
    return lstProyectosRama


def lstSoluciones(listado_soluciones):
    lstSolucionesRuta = [] 
    f = open(listado_soluciones, "r")
    f1 = f.readlines()
    for x in f1:
        lstSolucionesRuta.append(x)
    return lstSolucionesRuta 


def lstFolder():
    excluye = '__pycache__ ramas.py reporte.py listado_soluciones.txt componentes.py API-EH-MDC listado.csv'
    f = open("listado_soluciones.txt","w")
    with f:
        for x in os.listdir('.'):
            if not x in excluye: 
                varSln = getSln(x)
                f.write(x + ";" + varSln + "\n") 
        f.close()


def getSln(ruta):
    for file in os.listdir(ruta):
        if file.endswith(".sln"):
            print(os.path.join(ruta, file))
            return os.path.join(ruta, file)

if __name__ == "__main__":
    main(sys.argv)
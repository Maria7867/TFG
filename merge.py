#merge
from filesplit.merge import Merge
import os
import platform

def main():
    path_actual= os.getcwd()
    if platform.system()=="Windows":
        path_partes=path_actual+"\partes"
    if platform.system()=="Linux":
        path_partes=path_actual+"/partes"

    print("nombre: ")
    name_file=input()
    juntar = Merge(path_partes, path_actual, name_file)
    juntar.merge()

if __name__ == "__main__":
    main()

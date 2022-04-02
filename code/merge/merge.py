#merge
from filesplit.merge import Merge
import os
import platform

def mg_main():
    '''
    path_actual= os.getcwd()
    if platform.system()=="Windows":
        path_partes=path_actual+"\partes"
    if platform.system()=="Linux":
        path_partes=path_actual+"/partes"
    '''
    path_actual= os.getcwd()
    print("path of the folder with the file parts: ")
    path_partes=input()
    print("name of the merged file: ")
    name_file=input()
    juntar = Merge(path_partes, path_actual, name_file)
    juntar.merge()

#if __name__ == "__main__":
    #main()

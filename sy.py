#import dbx
#from prueba import pr
'''
from dbx import clientDP
from drive import client
#from mega import clientMU
from cliente import cl
from servidor import sv
from merge import merge
from decrypt import decrypt
'''
from code.dbx import clientDP
from code.drive import client
#from code.mega import clientMU
from code.cliente import cl
from code.servidor import sv
from code.merge import merge
from code.decrypt import decrypt

print("module: ")
module=input()

if module=='db':
    clientDP.dbx_main()
if module=='dv':
    client.dv_main()
#if module=='mu':
#    clientMU.mu_main()
if module=='cl':
    cl.cl_main()
if module=='sv':
    sv.sv_main()
if module=='merge':
    merge.mg_main()
if module=='decrypt':
    decrypt.dcy_main()
    #pr.p()

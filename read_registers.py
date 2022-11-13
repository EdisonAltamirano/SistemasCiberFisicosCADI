from pyModbusTCP.client import ModbusClient
import numpy as np
import time
myhost = "10.22.240.51"
myport = 12345
c = ModbusClient(host=myhost,port=myport)

class Missions:
    def read_info(self):
        if c.open():
            bits = c.read_holding_registers(0, 25)
            print(bits)
            time.sleep(1)
        else:
            print("unable to connect to "+myhost+":"+str(myport))
def mainloop():
    while True:
        mymission.read_info()
mymission=Missions()
 
mainloop()
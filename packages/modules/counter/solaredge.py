#!/usr/bin/python
import struct
from pymodbus.client.sync import ModbusTcpClient

from ...helpermodules import pub

def read_solaredge(counter):
    counter_num = counter.counter_num
    ipaddress = counter.data["config"]["config"]["solaredge"]["ip_address"]
    modbusport = 502
    slaveid = 1

    client = ModbusTcpClient(ipaddress, port=modbusport)

    resp= client.read_holding_registers(40206,5,unit=slaveid)
    value1 = resp.registers[0] 
    all = format(value1, '04x') 
    final = int(struct.unpack('>h', all.decode('hex'))[0]) * -1 

    sf = resp.registers[4] 
    sf = format(sf, '04x') 
    fsf = int(struct.unpack('>h', sf.decode('hex'))[0]) 
    if fsf == 4: 
        final = final * 10000 
    if fsf == 3: 
        final = final * 1000 
    if fsf == 2: 
        final = final * 100 
    if fsf == 1: 
        final = final * 10 
    if fsf == -1: 
        final = final / 10 
    if fsf == -2: 
        final = final / 100 
    if fsf == -3: 
        final = final / 1000 
    if fsf == -4: 
        final = final / 10000 

    pub.pub("openWB/set/counter/"+str(counter_num)+"/get/power_all", final) 

    resp= client.read_holding_registers(40194,2,unit=slaveid)
    multipli = resp.registers[0]
    multiplint = format(multipli, '04x')
    fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])
    resp= client.read_holding_registers(40191,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finala1 = int(struct.unpack('>h', all.decode('hex'))[0]) 
    resp= client.read_holding_registers(40192,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finala2 = int(struct.unpack('>h', all.decode('hex'))[0]) 
    resp= client.read_holding_registers(40193,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finala3 = int(struct.unpack('>h', all.decode('hex'))[0]) 

    resp= client.read_holding_registers(40194,2,unit=slaveid)
    mult2ipli = resp.registers[0]
    mult2iplint = format(mult2ipli, '04x')
    fmult2iplint = int(struct.unpack('>h', mult2iplint.decode('hex'))[0])

    if fmultiplint == fmult2iplint:
        if fmultiplint == 4:
            finala1 = finala1 * 10000
            finala2 = finala2 * 10000
            finala3 = finala3 * 10000
        if fmultiplint == 3:
            finala1 = finala1 * 1000
            finala2 = finala2 * 1000
            finala3 = finala3 * 1000
        if fmultiplint == 2:
            finala1 = finala1 * 100
            finala2 = finala2 * 100
            finala3 = finala3 * 100
        if fmultiplint == 1:
            finala1 = finala1 * 10
            finala2 = finala2 * 10
            finala3 = finala3 * 10
        if fmultiplint == 0:
            finala1 = finala1
            finala2 = finala2
            finala3 = finala3
        if fmultiplint == -1:
            finala1 = finala1 / 10
            finala2 = finala2 / 10
            finala3 = finala3 / 10
        if fmultiplint == -2:
            finala1 = finala1 / 100
            finala2 = finala2 / 100
            finala3 = finala3 / 100
        if fmultiplint == -3:
            finala1 = finala1 / 1000
            finala2 = finala2 / 1000
            finala3 = finala3 / 1000
        if fmultiplint == -4:
            finala1 = finala1 / 10000
            finala2 = finala2 / 10000
            finala3 = finala3 / 10000
        if fmultiplint == -5:
            finala1 = finala1 / 100000
            finala2 = finala2 / 100000
            finala3 = finala3 / 100000
    pub.pub("openWB/set/counter/"+str(counter_num)+"/get/current", [finala1, finala2, finala3])

    #voltage
    resp= client.read_holding_registers(40196,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finale1 = int(struct.unpack('>h', all.decode('hex'))[0])  / 100
    resp= client.read_holding_registers(40197,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finale2 = int(struct.unpack('>h', all.decode('hex'))[0])  / 100
    resp= client.read_holding_registers(40198,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finale3 = int(struct.unpack('>h', all.decode('hex'))[0])  / 100
    pub.pub("openWB/set/counter/"+str(counter_num)+"/get/voltage", [finale1, finale2, finale3])

    #watt pro phase
    resp= client.read_holding_registers(40207,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finale1 = int(struct.unpack('>h', all.decode('hex'))[0]) * -1 

    resp= client.read_holding_registers(40208,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finale2 = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
    resp= client.read_holding_registers(40209,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finale3 = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
    pub.pub("openWB/set/counter/"+str(counter_num)+"/get/power_phase", [finale1, finale2, finale3])

    #hz
    resp= client.read_holding_registers(40204,1,unit=slaveid)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    finalhz = int(struct.unpack('>h', all.decode('hex'))[0]) 

    resp= client.read_holding_registers(40205,1,unit=slaveid)
    multipli = resp.registers[0]
    multiplint = format(multipli, '04x')
    fmuliplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

    if fmultiplint == 4:
        finalhz = finalhz * 1000
    if fmultiplint == 3:
        finalhz = finalhz * 100
    if fmultiplint == 2:
        finalhz = finalhz * 10
    if fmultiplint == 1:
        finalhz = finalhz * 1
    if fmultiplint == 0:
        finalhz = finalhz  / 10
    if fmultiplint == -1:
        finalhz = finalhz / 100
    if fmultiplint == -2:
        finalhz = finalhz / 1000
    if fmultiplint == -3:
        finalhz = finalhz / 10000
    if fmultiplint == -4:
        finalhz = finalhz / 100000
    if fmultiplint == -5:
        finalhz = finalhz / 1000000

    pub.pub("openWB/set/counter/"+str(counter_num)+"/get/frequency", finalhz)

    #resp= client.read_holding_registers(40084,2,unit=1)
    #multipli = resp.registers[0]
    #multiplint = format(multipli, '04x')
    #fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

    #respw= client.read_holding_registers(40083,2,unit=1)
    #value1w = respw.registers[0]
    #allw = format(value1w, '04x')
    #rawprodw = finalw = int(struct.unpack('>h', allw.decode('hex'))[0]) * -1
    #if fmultiplint == -1:
    #    rawprodw = rawprodw / 10 
    #if fmultiplint == -2:
    #    rawprodw = rawprodw / 100
    #if fmultiplint == -3:
    #    rawprodw = rawprodw / 1000
    #if fmultiplint == -4:
    #    rawprodw = rawprodw / 10000
    #f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
    #f.write(str(rawprodw))
    #f.close()

    #resp= client.read_holding_registers(40093,2,unit=1)
    #value1 = resp.registers[0]
    #value2 = resp.registers[1]
    #all = format(value1, '04x') + format(value2, '04x')
    #final = int(struct.unpack('>i', all.decode('hex'))[0])
    #f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
    #f.write(str(final))
    #f.close()
    #pvkwhk= final / 1000
    #f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
    #f.write(str(pvkwhk))
    #f.close()

    resp= client.read_holding_registers(40234,2,unit=slaveid)
    value1 = resp.registers[0] 
    value2 = resp.registers[1] 
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0]) 
    pub.pub("openWB/set/counter/"+str(counter_num)+"/get/imported", final)

    resp= client.read_holding_registers(40226,2,unit=slaveid)
    value1 = resp.registers[0]
    value2 = resp.registers[1] 
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0])
    pub.pub("openWB/set/counter/"+str(counter_num)+"/get/exported", final)

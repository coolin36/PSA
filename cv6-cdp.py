#!/usr/bin/env python3

from scapy.all import *
import struct
from ctypes import *

def compute_cdp_checksum(cdp_bytes):
    checksum = 0
    paPaketLen = len(cdp_bytes)
    if(paPaketLen % 2 == 1):
        paddedData = bytearray(cdp_bytes + struct.pack("B", 0))

        # Swap bytes in last word
        paddedData[paPaketLen] = paddedData[paPaketLen-1]
        paddedData[paPaketLen-1] = 0

        # Compensate off-by-one error
        if(paddedData[paPaketLen] & 0x80):
            paddedData[paPaketLen] = paddedData[paPaketLen] - 1
            paddedData[paPaketLen-1] = paddedData[paPaketLen-1] - 1

    else:
        paddedData = cdp_bytes

    for i in range(0, paPaketLen, 2):
        checksum = checksum + paddedData[i] + (paddedData[i+1] << 8)
        if(checksum > 0xffff):
            checksum = checksum - 0xffff

    return c_ushort(~checksum).value

def mac_to_bytes(mac_str: str):
    mac_hex = mac_str.replace(":", "")
    return bytes.fromhex(mac_hex)

class Eth_frame():
    def __init__(self, src_mac):
        self._dst_mac = "01:00:0c:cc:cc:cc"
        self._src_mac = src_mac
        self._length = 0
        self._payload = None
    
    def add_payload(self, payload):
        self._payload = payload

    def to_bytes(self):
        payload_bytes = self._payload.to_bytes()
        self._length = len(payload_bytes)
        eth_bytes = mac_to_bytes(self._dst_mac) + mac_to_bytes(self._src_mac) + struct.pack("!H", self._length) 
        eth_bytes += payload_bytes
        return eth_bytes
    
class LLC():
    def __init__(self):
        self._dsap = 0xAA
        self._ssap = 0xAA
        self._ctrl = 0x03
        self._oui = "00000C"
        self._pid = 0x2000
        self._payload = None
    
    def add_payload(self, payload):
        self._payload = payload
    
    def to_bytes(self):
        return (struct.pack("!3B", self._dsap, self._ssap, self._ctrl) 
                + mac_to_bytes(self._oui) + struct.pack("!H", self._pid)
                + self._payload.to_bytes())
        
class CDP_hdr():
    def __init__(self):
        self._version = 1
        self._ttl = 180
        self._checksum = 0
        self._payload = list()

    def add_payload(self, payload):
        self._payload.append(payload)

    def to_bytes(self):
        cdp_bytes = struct.pack("!BBH", self._version, self._ttl, self._checksum)
        for i in self._payload:
            cdp_bytes += i.to_bytes()
        cdp_checksum = compute_cdp_checksum(cdp_bytes)

        return cdp_bytes[0:2] + struct.pack("H", cdp_checksum) + cdp_bytes[4:]
        
        
class TLV():
    def __init__(self, type):
        self._type = type
        self._length = 4
    
    def to_bytes(self):
        return struct.pack("!HH", self._type, self._length)
    
class Device_ID_TLV(TLV):
    def __init__(self, hostname):
        TLV.__init__(self, 0x0001)
        self._hostname = hostname

    def to_bytes(self):
        hostname_bytes = self._hostname.encode()
        self._length += len(hostname_bytes)
        return super().to_bytes() + hostname_bytes
    
class Software_TLV(Device_ID_TLV):
    def __init__(self, software_version):
        super().__init__(software_version)
        self._type = 0x0005

class Platform_TLV(Device_ID_TLV):
    def __init__(self):
        super().__init__("PVSA")
        self._type = 0x0006


def set_bit(in_var, bit_number):
    return in_var | 1 << bit_number-1
    # 0100
    # 0010
    # 0100


class Capabilities_TLV(TLV):
    def __init__(self, router=False, switch=False, host=True):
        TLV.__init__(self, 0x0004)
        self._length += 4
        self._capabilities = 0

        if router:
            self._capabilities = set_bit(self._capabilities, 1)
        if switch:
            self._capabilities = set_bit(self._capabilities, 4)  
        if host:
            self._capabilities = set_bit(self._capabilities, 5)

    def to_bytes(self):
        return TLV.to_bytes(self) + struct.pack("!I", self._capabilities)

if __name__ == "__main__":
    IFACES.show()

    iface = IFACES.dev_from_index(10)

    sock = conf.L2socket(iface=iface)

    eth = Eth_frame("00:11:22:33:44:55")
    llc = LLC()    
    cdp = CDP_hdr()
    tlv_dev = Device_ID_TLV("RA013-ucitel")
    cdp.add_payload(tlv_dev)
    tlv_cap = Capabilities_TLV(switch=True)
    cdp.add_payload(tlv_cap)
    tlv_soft = Software_TLV("Windows 11 Education x86_64 23H2")
    cdp.add_payload(tlv_soft)
    tlv_platform = Platform_TLV()
    cdp.add_payload(tlv_platform)
    llc.add_payload(cdp)
    eth.add_payload(llc)    
    eth_bytes = eth.to_bytes()

    sock.send(eth_bytes)
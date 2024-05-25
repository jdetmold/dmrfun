import socket
import struct

class Protocol:
    def __init__(self, buffer=None):
        self.buffer = buffer

    def id2ip(self, radio_id, cai=12):
        return f"{cai}.{(radio_id >> 16) & 0xff}.{(radio_id >> 8) & 0xff}.{radio_id & 0xff}"

class TMS(Protocol):
    def __init__(self, buffer=None):
        super().__init__(buffer)
        self.port = 5016

    def message_encode(self, msg):
        return msg.encode('utf-16le')

    def sendtoip(self, ipaddr, sms):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        message = self.message_encode(sms)
        length = len(message) + 8

        protocol = b'\x00' + struct.pack('!B', length) + b'\xe0\x00\x88\x04\r\x00\n' + message
        print(f"Sending to IP: {ipaddr}")
        print(f"Message Length: {length}")
        print(f"Protocol Header: {protocol[:8]}")
        print(f"Encoded Message: {message}")
        print(f"Full Protocol Message: {protocol}")
        sock.sendto(protocol, (ipaddr, self.port))
        sock.close()

    def sendtoid(self, cai, radioid, sms):
        ipaddr = self.id2ip(radioid, cai)
        print(f"Derived IP: {ipaddr} for Radio ID: {radioid}")
        self.sendtoip(ipaddr, sms)

def main():
    cai = 12
    destination_id = 147652
    message = "\x02" + "Hello, this is a test message."

    tms = TMS()
    tms.sendtoid(cai, destination_id, message)

if __name__ == "__main__":
    main()

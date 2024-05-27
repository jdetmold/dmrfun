import socket
import struct

class Protocol:
    def __init__(self, buffer=None):
        self.buffer = buffer

    def id2ip(self, radio_id, cai=12):
        # Calculate the IP address from the radio ID and CAI
        return f"{cai}.{(radio_id >> 16) & 0xff}.{(radio_id >> 8) & 0xff}.{radio_id & 0xff}"

class TMS(Protocol):
    def __init__(self, buffer=None):
        super().__init__(buffer)
        self.port = 4007

    def message_encode(self, msg):
        # Encode the message using UTF-16LE encoding
        return msg.encode('utf-16le')

    def sendtoip(self, ipaddr, sms):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        message = self.message_encode(sms)
        message_length = len(message)

        # Calculate the message length (second byte) as message length + 4
        protocol_header = bytearray([0x00, message_length + 4, 0xc0, 0x00, 0x83, 0x04])
        protocol = bytes(protocol_header) + message

        print(f"Sending to IP: {ipaddr}")
        print(f"Message Length: {message_length}")
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
    message = "Hello, this is a test message. 123456"  # Removed unnecessary control character

    tms = TMS()
    tms.sendtoid(cai, destination_id, message)

if __name__ == "__main__":
    main()

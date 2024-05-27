import socket
import threading
import time

class TMS:
    def __init__(self):
        self.source_port = 4007
        self.destination_port = 4007
        self.cai = 12
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.source_port))

    def id2ip(self, radio_id):
        return f"{self.cai}.{(radio_id >> 16) & 0xff}.{(radio_id >> 8) & 0xff}.{radio_id & 0xff}"

    def send_message(self, radio_id, message):
        ip_addr = self.id2ip(radio_id)
        message = message.encode('utf-16le')
        message_length = len(message) + 4

        header = bytearray([0x00, message_length, 0xc0, 0x00, 0x83, 0x04])
        packet = bytes(header) + message

        self.sock.sendto(packet, (ip_addr, self.destination_port))
        print(f"Message sent to {ip_addr} from port {self.source_port}")

    def listen_for_ack(self):
        print("Listening for ACK...")
        data, addr = self.sock.recvfrom(1024)
        print(f"ACK received from {addr}: {data}")
        self.sock.close()

def main():
    tms = TMS()
    destination_id = 147652
    message = "Hello, this is a test message."

    listener_thread = threading.Thread(target=tms.listen_for_ack)
    listener_thread.start()
    time.sleep(1)

    tms.send_message(destination_id, message)

    listener_thread.join()

if __name__ == "__main__":
    main()

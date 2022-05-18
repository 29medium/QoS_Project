import socket
from probe import Probe
import time

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1",8080))

    s.listen(1)
    conn, addr = s.accept()

    while True:
        try:
            # Latencia
            data = conn.recv(1024)

            if not data: break
            
            p = Probe(data,None)
            conn.sendall(Probe(1,p.timestamp).toBytes())

        except socket.error:
            print("Error")
            break
    
    conn.close()
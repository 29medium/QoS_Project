import socket
from probe import Probe
import time

def latencia(s):
    lats = []

    for i in range(0,100):
        s.sendall(Probe(1,time.perf_counter()).toBytes())
        data = s.recv(1024)
        p = Probe(data)

        lats.append((time.perf_counter() - p.timestamp) * 1000)

    lat = sum(lats) / len(lats)
    
    jitter = 

    return lat, 

if __name__ == "__main__":
    
    #Latencia 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1",8080))

    print("Latencia: " + str(format(lat_med, ".3f")) + " ms")
    print("Jitter: " + str(format(jitter_1_2, ".3f")) + " ms")

    s.close
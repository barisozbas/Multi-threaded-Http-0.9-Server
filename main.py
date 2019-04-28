import os
import socket
import myThread
import sys

def main():
 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.bind((HOST,PORT))
        soc.listen(10)

        while True:
            conn,address = soc.accept()
            myThread.myThread(conn, address, dir).start()


if __name__ == "__main__":
    HOST = "0.0.0.0"

    if sys.argv[1:]:
        PORT = int(sys.argv[1])
    else:
        PORT = 8080

    if sys.argv[2:]:
        os.chdir(sys.argv[2])

    dir = os.getcwd()

    main()
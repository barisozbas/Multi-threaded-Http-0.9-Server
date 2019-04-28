import threading
import datetime
now = datetime.datetime.now()

class myThread(threading.Thread):
    def __init__(user,channel,address, dir_r):
        dir = dir_r
        user.channel = channel
        user.address = address
        global log
        log = open(dir+"\{}.txt".format(now.date()), "a")
        threading.Thread.__init__(user)
     
    def run(user):
        req = user.channel.recv(1024)
        packet,object = user.reqParser(req)
        user.channel.sendall(packet)
        user.channel.close()

    def reqParser(user,req):
        temp = req.split(b'\r\n')
        object = str(temp[0][4:-9])[2:-1]
        info = str(user.channel)
        info = info[92:][:-1]
        if (object == "" or object == '.' or object == "/" ):
            object = "/index.html"

        printval = "{}      GET {} {}".format(now,object,info)
        print(printval)

        log.write("{}\r\n".format(printval))
        temp_obj = ".{}".format(object)
        objectStatus = "404 Not Found"
        try:
            objectBuffer = open(temp_obj ,'rb').read()
            objectStatus = "200 OK"
        except (PermissionError, FileNotFoundError) as e:
            objectBuffer = open("404.html", 'rb').read()
            
            
        
        
        objectLength = len(objectBuffer)
        #objectLength = objectLength.to_bytes(2, byteorder='big')
        objectLength = objectLength.to_bytes((objectLength.bit_length() // 8) + 1,'little')
        #packet = b'HTTP/0.9 %b\r\nContent-Type: test/html\r\ncharset = utf-8\r\nContent-length: %b\r\n\r\n%b' % (bytes(objectStatus,encoding='utf-8'),objectLength,objectBuffer)
        objExt = ""
        try:
            temp = object.split(".")
            objExt = temp[1]
        except IndexError:
            pass
        if(objExt == "jpg"):
            packet = b'HTTP/0.9 200 OK\r\nContent-Length: %b\r\nContent-Type: image/jpg\r\ncharset=UTF-8\r\n\r\n%b' % (objectLength,objectBuffer)
        else:
            packet = b'HTTP/0.9 200 OK\r\nContent-Length: %b\r\nContent-Type: text/html\r\ncharset=UTF-8\r\n\r\n%b' % (objectLength,objectBuffer)
        
        #packet = bytes(packet,"UTF-8")
        #print(packet)
        return packet,object
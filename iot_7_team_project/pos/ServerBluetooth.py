#-*- coding: utf-8 -*-
import os
import sys
import time
import json
import struct
import bluetooth
import httplib, urllib
import bluetooth._bluetooth as bluez
from bluetooth.ble import DiscoveryService

reload(sys)
sys.setdefaultencoding('utf-8')


hostMACAddress = 'B8:27:EB:67:3F:85' 
port = 5
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))

json_obj = 0

def get_now():
    now = time.localtime()
    r = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return r

def send_order():
    global json_obj
    params = urllib.urlencode({"time":get_now()})
    headers = {"Content-type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection("iot.hanpyo.com:3000")
    conn.request("POST","/orders",params,headers)
    
    res = conn.getresponse()
    #print response.status, response.reason 200 OK
    data = res.read().decode("utf-8")
    json_obj = json.loads(data)
    conn.close()
    print(json_obj["_id"])

def send_product(product):
    global json_obj
    params = urllib.urlencode({"name":product,"price":""})
    headers = {"Content-type":"application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection("iot.hanpyo.com:3000")
    conn.request("POST","/orders/"+json_obj["_id"]+"/products",params,headers)

    #res = conn.getresponse()
    #print response.status, response.reason 200 OK
    #data = res.read().decode("utf-8")
    #conn.close()
    #print(data)


while True:
    print "listen"
    s.listen(backlog)
    try:
        print "start"
        client, clientInfo = s.accept()
        print "link on"
        while 1:
            b_data = client.recv(size)
            if b_data:
                print(b_data)
                count = int(b_data)
                #send_order()
                arr = []
                for i in range(0, count):
                    b_data = client.recv(size)
                    if b_data:
                        print(b_data)
                        arr.append(b_data)                      
                    #send_product(b_data)
                send_order()
                print "http send"
                for i in range(0, count):
                    send_product(arr[i])
                    
                #client.send(b_data) 
    except:	
        print("Closing socket")
        client.close()
        s.close()

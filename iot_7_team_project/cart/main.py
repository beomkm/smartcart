#-*- coding: utf-8 -*-
import sys
import time
import socket
import tkFont
import threading
import bluetooth
import tkMessageBox
from Tkinter import *
import RPi.GPIO as gpio

reload(sys)
sys.setdefaultencoding('utf-8')


def ipc_read():
    global product
    while ipc_flag:
        data = ipc_sock.recv(256)
        if data == "":
            break
        print("received : ", repr(data))
        try:
            rssi = int(data)
        except ValueError:
            continue
        if rssi > -45:
            selection = 0
            draw_btn2(0)
            while True:
                if gpio.input(16) == 1:
                    draw_btn2(2)
                    selection = 2
                elif gpio.input(21) == 1:
                    draw_btn2(1)
                    selection = 1
                if gpio.input(20) and selection != 0:
                    break
                time.sleep(0.1)
            canvas.delete("all")
            if selection == 1:         
                summation = 0
                blu_sock.send(str(len(p_list)+2))
                for i in p_list.keys(): 
                    summation += p_list[i][1]
                    element = "%-12s %2dea %8dwon"%(i, p_list[i][0], p_list[i][1])
                    blu_sock.send(element)
                blu_sock.send("=======================")
                blu_sock.send(unicode("총액 : ")+str(summation))
                draw_complete()
                break

def and_read():
    global product
    print("Waiting for connection...")
    and_con, and_addr = and_sock.accept()
    print("Connected", and_addr)    
    while and_flag:
        data = and_con.recv(1024)
        if data == "":
            and_con.close()
            print("Waiting for connection...")
            and_con, and_addr = and_sock.accept()
            print("Connected", and_addr)    
        print("received", repr(data))
        code = repr(data)
        code = code[1:-3]
        product = dic.get(code, 0)
        if product == 0:
            continue
        saved = p_list.get(product[0], 0)
        if saved == 0:
            p_list[product[0]] = [1, product[1]]
        else:
            draw_btn(0)
            selection = 0
            while True:
                if gpio.input(16) == 1:
                    draw_btn(2)
                    selection = 2
                elif gpio.input(21) == 1:
                    draw_btn(1)
                    selection = 1
                if gpio.input(20) and selection != 0:
                    break
                time.sleep(0.1)
            canvas.delete("all")
            if selection == 1:
                p_list[product[0]][0] += 1
                p_list[product[0]][1] += product[1]
            elif selection == 2:
                p_list[product[0]][0] -= 1
                p_list[product[0]][1] -= product[1]
                if p_list[product[0]][0] <= 0:
                    p_list.pop(product[0], None)
        listbox.delete(0, END)

        element = "%-12s %2s %6s"%(unicode("상품명"), unicode("개수"), unicode("가격"))
        listbox.insert(END, element)
        summation = 0
        for i in p_list.keys(): 
            summation += p_list[i][1]
            element = "%-12s %2d %8d"%(i, p_list[i][0], p_list[i][1])
            listbox.insert(END, element)
        listbox.insert(END, "===========================")
        listbox.insert(END, unicode("합계 : ") + str(summation))


def draw_complete():
    canvas.create_text(110, 127, text=unicode("결제완료"), font=tkFont.Font(size=17, weight='bold'))
 

def draw_btn_bg(state):
    if state == 0:
        canvas.create_rectangle(50,50,150,100,fill="gray")
        canvas.create_rectangle(50,150,150,200,fill="gray")
    elif state == 1:
        canvas.create_rectangle(50,50,150,100,fill="green")
        canvas.create_rectangle(50,150,150,200,fill="gray")
    elif state == 2:
        canvas.create_rectangle(50,50,150,100,fill="gray")
        canvas.create_rectangle(50,150,150,200,fill="green")

def draw_btn(state):
    draw_btn_bg(state)
    canvas.create_text(100, 77, text=unicode("추가"), font=tkFont.Font(size=15, weight='bold'))
    canvas.create_text(100, 177, text=unicode("제거"), font=tkFont.Font(size=15, weight='bold'))

def draw_btn2(state):
    draw_btn_bg(state)
    canvas.create_text(100, 77, text=unicode("결제"), font=tkFont.Font(size=15, weight='bold'))
    canvas.create_text(100, 177, text=unicode("취소"), font=tkFont.Font(size=15, weight='bold')) 

dic = {
"4903333185016":[unicode("초콜릿"),1800],
"8801062331819":[unicode("목캔디"),650],
"8801094363000":[unicode("파워에이드"),800]}

p_list = {}


gpio.setmode(gpio.BCM)
gpio.setup(12 ,gpio.OUT)
gpio.setup(16 ,gpio.IN)
gpio.setup(20 ,gpio.IN)
gpio.setup(21 ,gpio.IN)
gpio.output(12, 1)

blu_host = "B8:27:EB:67:3F:85"
blu_port = 5
blu_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
blu_sock.connect((blu_host, blu_port))

ipc_host = "127.0.0.1"
ipc_port = 13579
ipc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipc_sock.connect((ipc_host, ipc_port))
ipc_flag = True
ipc_th = threading.Thread(target=ipc_read)
ipc_th.start()

and_host = ""
and_port = 24680
and_flag = True
and_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
and_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
and_sock.bind((and_host, and_port))
and_sock.listen(1)
and_th = threading.Thread(target=and_read)
and_th.start()

product = "0000"
canvas = 0

frame = Tk()

label = Label(frame, text=unicode("IoT 7조 스마트카트"))
label.pack()

scroll = Scrollbar(frame, orient=VERTICAL)
canvas = Canvas(frame, width=200)
listbox = Listbox(frame)
listbox.config(width=10, height=5, font=tkFont.Font(size=14))

scroll.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT)
listbox.pack(side=LEFT, fill=BOTH, expand=1)
"""
for i in range(0, 10):
    listbox.insert(END, unicode("p")+str(i))
"""

listbox.config(yscrollcommand=scroll.set)
scroll.config(command=listbox.yview)


#listbox.selection_set(4)


frame.attributes("-fullscreen", True)

try:
    mainloop()
except KeyboardInterrupt as e:
    ipc_flag = False
    and_flag = False



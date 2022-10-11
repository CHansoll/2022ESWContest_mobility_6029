import socket
import time

# initializing count data
count_acc = count_bump = count_uphill = count_downhill = count_winter = count_overcharge = count_overdischarge = count_overcurrent = count_total = 0

# connect to the server raspberry pi to use socket communication
HOST = '192.168.137.60'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# select type of count
def switch(i):
    switcher = {
        0: 'uphill',
        1: 'downhill',
        2: 'bump',
        3: 'winter',
        4: 'overcharge',
        5: 'overdischarge',
        6: 'overcurrent'
    }
    return switcher.get(str, 'ooo')


# select type of count
def cmd(i):
    command = switch(i)
    client_socket.sendall(command.encode())


# sending count data to the server
def senddata(count_uphill, count_downhill, count_bump, count_winter, count_overcharge, count_overdischarge,
             count_overcurrent):
    command = str(count_uphill)
    client_socket.sendall((command.encode()))
    time.sleep(0.1)

    command = str(count_downhill)
    client_socket.sendall((command.encode()))
    time.sleep(0.1)

    command = str(count_bump)
    client_socket.sendall((command.encode()))
    time.sleep(0.1)

    command = str(count_winter)
    client_socket.sendall((command.encode()))
    time.sleep(0.1)

    command = str(count_overcharge)
    client_socket.sendall((command.encode()))
    time.sleep(0.1)

    command = str(count_overdischarge)
    client_socket.sendall((command.encode()))
    time.sleep(0.1)

    command = str(count_overcurrent)
    client_socket.sendall((command.encode()))
    time.sleep(0.1)





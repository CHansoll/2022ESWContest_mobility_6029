import socket
import Display
import os
import matplotlib.pyplot as plt
from twilio.rest import Client

HOST = '192.168.137.60'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()

client_socket, addr = server_socket.accept()
print('Connected by', addr)
# Socket communication connection with client


count_list = []
count = 0


# Creating a Count Array for each situation

# send result analysis message
def message(count_list):
    max_index = count_list.index(max(count_list))

    if max_index == 0:
        uphill = max_index
        avoid = "uphill"
    elif max_index == 1:
        downhill = max_index
        avoid = "downhill"
    else:
        bump = max_index
        avoid = "speed bump"

    if count_list[0] == count_list[1] == count_list[2]:
        bump = max_index
        avoid = "speed bump"
    if count_list[0] > count_list[2] and count_list[0] == count_list[1]:
        bump = max_index
        avoid = "speed bump"
    if count_list[1] > count_list[2] and count_list[0] == count_list[1]:
        downhill = max_index
        avoid = "downhill"

    # user's twilio account_sid
    account_sid = 'AC0c05647c7d4a5866f9fe34c0dfbda77f'

    # user's twilio auth_token
    auth_token = 'c70a70cab40b438a94883503fbc31b4e'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        # user's phone number
        to="+8201027479418",

        # user's twilio phone number
        from_="+12317155830",
        body="\nThere is a possibility of an internal battery defect. Please visit nearby repair shop ASAP" if (
                                                                                                                           count_list[
                                                                                                                               4] +
                                                                                                                           count_list[
                                                                                                                               5] +
                                                                                                                           count_list[
                                                                                                                               6]) >= 1 else "\nThe current temperature is below minus 7 degrees Celsius. Avoid long-term parking outdoors, as the performance of the battery may deteriorate." if
        count_list[3] >= 1 else "\nuphill count: " + str(count_list[0]) + " times\ndownhill count: " + str(
            count_list[1]) + " times\nspeed bump count: " + str(count_list[
                                                                    2]) + " times\n\nThere is a possibility that the " + avoid + " caused deterioration of the battery performance. Please be careful when driving over " + avoid + ".")


while True:

    data = client_socket.recv(1024)

    if str.isdigit(
            data.decode()):  # When a number is recieved from a client, it is judged as count information and stored in a count array
        count_list.append(int(data.decode()))

        if len(count_list) == 7:  # When count information for all eight situations is received, a ratio graph is displayed based on it
            count = count + 1

            print(count_list)
            budget_data = [count_list[0], count_list[1], count_list[2]]
            budget_cat = ['uphill', 'downhill', 'bump']
            plt.pie(budget_data, labels=budget_cat)
            fig = plt.gcf()
            fig.set_size_inches(5, 2)
            plt.show()
            message(count_list)
            count_list = []
            if count == 3:
                server_socket.close()
                break

    else:  # When information other than count information (information on what situation it is) is received, a warning window is displayed

        display.Display(data.decode())
        print(data.decode())


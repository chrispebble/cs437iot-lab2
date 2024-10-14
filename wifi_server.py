# Christopher Rock (cmrock2)
# CS 437 IOT Fall 2024
# Lab 2: LTE: Self-Driving Car - Networking

import socket
import server_control_car as scc
import datetime


HOST = "192.168.1.80"  # IP address of your Raspberry PI
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
keep_running = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Listening on", HOST, ":", PORT)

    client = None

    try:

        while keep_running:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)  # receive 1024 Bytes of message in binary format
            if data != b"":
                cmd = data.decode("utf-8").strip()
                response = ""
                if cmd == "left":
                    response = "go left"
                    scc.left_turn()
                elif cmd == "right":
                    response = "go right"
                    scc.right_turn()
                elif cmd == "forward":
                    response = "go forward"
                    scc.move_forward()
                elif cmd == "back":
                    response = "go back"
                    scc.move_backward()
                elif cmd == "status":
                    response = scc.get_status()
                else:
                    response = "No match:" + cmd

                print(response)

                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                response_with_timestamp = f"{timestamp} - {response}"

                client.sendall(
                    response_with_timestamp.encode("utf-8")
                )  # Echo back to client

    except KeyboardInterrupt:
        keep_running = False

    finally:
        print("Closing socket")
        if client:
            client.close()
        s.close()

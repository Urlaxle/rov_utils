#!/bin/python3
import socket
import time 
import click 
import sys

@click.command()
@click.option("--host", default="127.0.0.1", help="Host interface to start server on.")
@click.option("--port", default=5000, help="Port number to start server on.")
@click.option("--interval", default=1, help="Time interval to send data in seconds.")
@click.option("--filename", default="data.txt", help="File containing data to be sent.")
@click.option("--multi_message", default=False, help="File contains multiple messages.")
@click.option("--delimiter", default="\n", help="End of message delimiter.")
@click.option("--loop", default=True, help="Loop data from file.")

def start_server(host, port, interval, filename, multi_message, delimiter, loop):
    """
    Summary:
    This function starts a TCP server that listens on the specified host and port.
    The server reads data from a specified file and sends it to connected clients.
    The data can be sent as a single message or multiple messages based on the 
    `multi_message` flag. If `multi_message` is True, the file is split into 
    multiple messages using the specified delimiter. The server can loop the data 
    indefinitely if the `loop` flag is set to True. The interval between sending 
    messages can be controlled using the `interval` parameter.

    Parameters:
    - host (str): Host interface to start server on.
    - port (int): Port number to start server on.
    - interval (int): Time interval to send data in seconds.
    - filename (str): File containing data to be sent.
    - multi_message (bool): File contains multiple messages.
    - delimiter (str): End of message delimiter.
    - loop (bool): Loop data from file.
    """

    # Start server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")

                # Data based on multi message or not
                try:
                    with open(filename, "r") as f:
                        data = f.read()
                except Exception as e:
                    print(f"Error: {e}")
                    sys.exit(0)
                
                if multi_message:
                    data = data.split(delimiter)
                
                # Send data with interval
                if loop:
                    while True:
                        if not multi_message:
                            conn.sendall(data.encode())
                            time.sleep(interval)
                        else:
                            for line in data:
                                conn.sendall(line.encode())
                                time.sleep(interval)
                else:
                    if not multi_message:
                        conn.sendall(data.encode())
                    else:
                        for line in data:
                            conn.sendall(line.encode())
                            time.sleep(interval)

if __name__ == "__main__":
    start_server()
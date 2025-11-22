# server.py
"""
TCP server for student assignment, with handshake, data transfer, teardown.
"""

import socket
from common import log_event

LOGFILE = "tcp_log_S.json"

def run_server(host="127.0.0.1", port=9000):

    # Clear old log
    with open(LOGFILE, "w") as f:
        f.write("")

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host, port))
    server_sock.listen(1)
    print(f"Server listening on {host}:{port}")

    conn, addr = server_sock.accept()
    print(f"Connected by {addr}")

    seq_server = 500

    while True:
        data = conn.recv(2048).decode()
        if not data:
            break

        # Format: FLAG,SEQ,ACK,DATA(optional)
        parts = data.split(",", 3)
        flag = parts[0]
        seq_client = int(parts[1])
        ack_client = int(parts[2])
        payload = parts[3] if len(parts) > 3 else ""

        log_event(LOGFILE, "Client", "Server", seq_client, ack_client, flag)

        # ---------------------------
        #   HANDSHAKE
        # ---------------------------
        if flag == "SYN":
            # SYN actions: send "SYN-ACK”, caculate seq_num, ack_num, logfile


        elif flag == "ACK":
            continue

        # ---------------------------
        #   DATA Receive
        # ---------------------------
        elif flag == "DATA":
            print("SERVER RECEIVED DATA:", payload)
            # Return ACK and caculate seq_num, ack_num, logfile

        # ---------------------------
        #   TEARDOWN
        # ---------------------------
        elif flag == "FIN":
            # Return ACK and caculate seq_num, ack_num, logfile
            # Send Fin, and logfile
            print("Fin")

        else:
            continue

    conn.close()
    server_sock.close()
    print("Server closed.")


if __name__ == "__main__":
    run_server()

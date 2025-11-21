# student_assignment.py
"""
Student assignment: implement handshake, send data, teardown.
"""

from common import log_event
import socket

LOGFILE = "tcp_log_C.json"

def tcp_handshake(client_sock, seq, ack):
    # Send SYN
    client_sock.send(f"SYN,{seq},{ack}".encode())
    log_event(LOGFILE, "Client", "Server", seq, ack, "SYN")
    seq += 1

    # Receive SYN-ACK
    flag, s_seq, s_ack = client_sock.recv(1024).decode().split(",")
    log_event(LOGFILE, "Server", "Client", int(s_seq), int(s_ack), flag)

    # Send ACK
    client_sock.send(f"ACK,{seq},{int(s_seq)+1}".encode())
    log_event(LOGFILE, "Client", "Server", seq, int(s_seq)+1, "ACK")

    return seq, int(s_seq)+1


def tcp_send_data(client_sock, seq, ack, data):
    """
    Send application data with DATA flag.
    """
    # Send DATA
    client_sock.send(f"DATA,{seq},{ack},{data}".encode())
    log_event(LOGFILE, "Client", "Server", seq, ack, "DATA")

    seq += len(data)

    # Receive ACK for data
    flag, s_seq, s_ack = client_sock.recv(2048).decode().split(",")
    log_event(LOGFILE, "Server", "Client", int(s_seq), int(s_ack), flag)

    return seq, int(s_ack)


def tcp_teardown(client_sock, seq, ack):

    # Send FIN
    client_sock.send(f"FIN,{seq},{ack}".encode())
    log_event(LOGFILE, "Client", "Server", seq, ack, "FIN")
    seq += 1

    # Receive ACK
    flag, s_seq, s_ack = client_sock.recv(1024).decode().split(",")
    log_event(LOGFILE, "Server", "Client", int(s_seq), int(s_ack), flag)

    # Receive FIN
    flag, s_seq, s_ack = client_sock.recv(1024).decode().split(",")
    log_event(LOGFILE, "Server", "Client", int(s_seq), int(s_ack), flag)

    # Send final ACK
    client_sock.send(f"ACK,{seq},{int(s_seq)+1}".encode())
    log_event(LOGFILE, "Client", "Server", seq, int(s_seq)+1, "ACK")


def run_client(host="127.0.0.1", port=9000, data="IMC Welcome!"):
    with open(LOGFILE, "w") as f:
        f.write("")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    seq = 100
    ack = 0

    # 1 handshake
    seq, ack = tcp_handshake(sock, seq, ack)
    # 2 data transfer (stop and wait)
    for data_ in data:
        seq, ack = tcp_send_data(sock, seq, ack, data_)

    # 3 teardown
    tcp_teardown(sock, seq, ack)

    sock.close()


if __name__ == "__main__":
    run_client()

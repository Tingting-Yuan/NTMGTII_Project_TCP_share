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

    # Send ACK

    # log every step

    return seq, ack_num


def tcp_send_data(client_sock, seq, ack, data):
    """
    Send application data with DATA flag.
    """
    # Send DATA

    # Receive ACK for data

    # logfile
    log_event(LOGFILE, "Server", "Client", int(s_seq), int(s_ack), flag)

    return seq, int(s_ack)


def tcp_teardown(client_sock, seq, ack):

    # Send FIN

    # Receive ACK

    # Receive FIN

    # Send final ACK
    
    # log every step
    
    


def run_client(host="127.0.0.1", port=9000, data="IMC Welcome!"):
    with open(LOGFILE, "w") as f:
        f.write("")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    # start num, can be any num.
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

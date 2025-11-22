# Networking Technologies and Management Systems II
### Simple TCP Messaging Protocol — Programming Project
### Programming Project (WS 2025/26)

Project Overview

This project implements a simplified version of TCP at the application layer using Python sockets.
Students must complete the minimal functionality of a TCP-like protocol by extending:

- server.py
- client.py

## The goal is to demonstrate understanding of:

1. TCP three-way handshake (10 points)
   - Client → Server: SYN, seq=x
   - Server → Client: SYN-ACK, seq=y, ack=x+1
   - Client → Server: ACK, seq=x+1, ack=y+1

2. Reliable data transmission using Stop-and-Wait ARQ (10 points)

   Client sends a list of data strings sequentially: e.g., ["Hello!", "IMC Server!", "Pleased to visit the server!", "See you next time!"]
   - Client → Server: Data
   - Server → Client: ACK

3. TCP four-way teardown (10 points)
   -  Client → Server: FIN
   -  Server → Client: ACK
   -  Server → Client: FIN
   -  Client → Server: ACK

4. Correct sequence number (SEQ) and acknowledgement number (ACK) handling (10 points)

All transmitted messages are logged into JSON files and automatically validated by GitHub Actions + pytest.


📁 File Structure
project/
  - │── client.py
  - │── server.py
  - │── common.py        # logfile formate
  - │── test.py          # Instructor-provided automated tests
  - │── tcp_log_S.json   # Server logs
  - │── tcp_log_C.json   # Client logs
  - │── .github/workflows/tcp-test.yml
  - │── README.md


🗂 Logging Format (given in common.py)

Every message must be logged as a JSON line, e.g.:

{"from": "Client", "to": "Server", "seq": 107, "ack": 107, "flags": "DATA", "timestamp": 1763736650.633416}

Note: don't change test.py and test.yml

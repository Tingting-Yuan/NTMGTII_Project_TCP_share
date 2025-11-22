# test.py
"""
Automated test for student's TCP assignment.
Checks:
1. 3-way handshake
2. Data transfer (DATA_STRING)
3. 4-way teardown
"""

import json
import pytest
from server import run_server
from client import run_client
import threading
import time
import socket
import logging



LOGFILE = "tcp_log_S.json"
LOGFILE_C = "tcp_log_C.json"
DATA_STRING = ["Hello!", "IMC Server!", "Pleased to visit the server!", "See you next time!"]

# === SCORE CALCULATION === #
TOTAL_SCORE = 0

def add_score(points):
    global TOTAL_SCORE
    TOTAL_SCORE += points

def load_events():
    """Load JSON events from log file, skip empty lines."""
    events = []
    with open(LOGFILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
    return events

def test_run():
    with open(LOGFILE, "w") as f:
        f.write("")
    with open(LOGFILE_C, "w") as f:
        f.write("")
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    time.sleep(0.2)  # Wait server to start

    result = run_client(data=DATA_STRING)  # connect & handshake


def test_handshake():
    """Check TCP 3-way handshake: SYN → SYN-ACK → ACK."""
    global TOTAL_SCORE
    try:
        events = load_events()

        # Filter handshake packets
        hs = [e for e in events if e["flags"] in ("SYN", "SYN-ACK", "ACK")]

        # Must have at least 3 events
        assert len(hs) >= 3, "Handshake incomplete"

        # Check order
        assert hs[0]["flags"] == "SYN", "Client must start with SYN"
        assert hs[1]["flags"] == "SYN-ACK", "Server must respond with SYN-ACK"
        assert hs[2]["flags"] == "ACK", "Client must finish with ACK"
        add_score(10)

        # Basic seq/ack correctness
        assert hs[1]["ack"] == hs[0]["seq"] + 1, "Server ACK must acknowledge SYN"
        assert hs[2]["ack"] == hs[1]["seq"] + 1, "Client ACK must acknowledge SYN-ACK"
        print("3-way Handshake check passed ✅")
        add_score(5)
    except:
        print("\n3-way Handshake check failed")
        pass


def test_multiple_data_segments():
    """
    Test multiple DATA segments from client:
    1. Ensure there are multiple DATA events.
    2. Check client SEQ increments correctly according to DATA length.
    3. Check server ACK confirms all client data.
    """
    global TOTAL_SCORE
    try:
        events = load_events()

        # Extract client DATA events
        datas = [x for x in events if x["from"] == "Client" and x["flags"] == "DATA"]
        assert len(datas) >= 2, "Should have at least 2 DATA segments"

        # Check client SEQ increments correctly
        for i in range(1, len(datas)):
            prev_seq = datas[i-1]["seq"]
            prev_len = len(DATA_STRING[i-1])      # Use length of previous DATA
            expected_seq = prev_seq + prev_len
            assert datas[i]["seq"] == expected_seq, \
                f"Client SEQ mismatch for DATA {i}: expected {expected_seq}, got {datas[i]['seq']}"

        # Extract server ACK events
        ack_events = [e for e in events if e["from"] == "Server" and e["flags"] == "ACK"]

        # Check each DATA is acknowledged correctly
        for i, data_event in enumerate(datas):
            expected_ack = data_event["seq"] + len(DATA_STRING[i])
            ack_found = any(ack["ack"] == expected_ack for ack in ack_events)
            assert ack_found, f"Server ACK missing for DATA {i}: expected ack={expected_ack}"
        add_score(5)
        print("Data Sent: sequence check passed ✅")
        add_score(10)
    except:
        print("Data sent check failed")
        pass



def test_teardown():
    """Check 4-way teardown: FIN → ACK → FIN → ACK."""
    global TOTAL_SCORE
    try:
        events = load_events()

        teardown = [e for e in events if e["flags"] in ("FIN", "ACK")]

        # At least 4 teardown-relevant events
        assert len(teardown) >= 4, "Teardown must include FIN/ACK sequence"

        # Extract only flags
        flags = [e["flags"] for e in teardown]

        # Expected minimal sequence:
        # Client FIN → Server ACK → Server FIN → Client ACK
        assert "FIN" in flags, "Client must send FIN"
        assert flags.count("FIN") >= 2, "Should have at least 2 FINs (client + server)"
        assert flags.count("ACK") >= 2, "Should have at least 2 ACKs"

        # Ordering check (not too strict)
        # First FIN must be from client
        first_fin = None
        for e in teardown:
            if e["flags"] == "FIN":
                first_fin = e
                break

        assert first_fin is not None, "No FIN found"
        assert first_fin["from"] == "Client", "First FIN must come from client"

        # Last ACK must come from client (final ACK)
        last_ack = None
        for e in reversed(teardown):
            if e["flags"] == "ACK":
                last_ack = e
                break

        assert last_ack is not None, "No ACK found"
        assert last_ack["from"] == "Client", "Final ACK must come from client"

        print("4-way teardown check passed ✅")
        add_score(10)
    except:
        print("4-way teardown check failed")
        pass

def test_show_final_score():
    print("\n==============================")
    print(f"FINAL SCORE: {TOTAL_SCORE} / 40")
    print("==============================\n")

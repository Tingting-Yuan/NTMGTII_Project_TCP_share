# common.py
import json
import time

def log_event(logfile, sender, receiver, seq, ack, flags):
    """TCP event logfile"""
    event = {
        "from": sender,
        "to": receiver,
        "seq": seq,
        "ack": ack,
        "flags": flags, #"SYN", "SYN-ACK", "ACK", "DATA", "FIN"
        "timestamp": time.time()
    }
    with open(logfile, "a") as f:
        f.write(json.dumps(event) + "\n")


# An example of logflie:
# {"from": "Client", "to": "Server", "seq": 201, "ack": 10, "flags": "SYN", "timestamp": 1763765829.417347}
# {"from": "Server", "to": "Client", "seq": 101, "ack": 202, "flags": "SYN-ACK", "timestamp": 1763765829.418596}
# {"from": "Client", "to": "Server", "seq": 202, "ack": 102, "flags": "ACK", "timestamp": 1763765829.4188569}
# {"from": "Client", "to": "Server", "seq": 202, "ack": 102, "flags": "DATA", "timestamp": 1763765829.419067}
# {"from": "Server", "to": "Client", "seq": 102, "ack": 208, "flags": "ACK", "timestamp": 1763765829.4196281}
# {"from": "Client", "to": "Server", "seq": 208, "ack": 208, "flags": "DATA", "timestamp": 1763765829.419827}
# {"from": "Server", "to": "Client", "seq": 103, "ack": 219, "flags": "ACK", "timestamp": 1763765829.4202409}
# {"from": "Client", "to": "Server", "seq": 219, "ack": 219, "flags": "DATA", "timestamp": 1763765829.420415}
# {"from": "Server", "to": "Client", "seq": 104, "ack": 247, "flags": "ACK", "timestamp": 1763765829.420807}
# {"from": "Client", "to": "Server", "seq": 247, "ack": 247, "flags": "DATA", "timestamp": 1763765829.421042}
# {"from": "Server", "to": "Client", "seq": 105, "ack": 265, "flags": "ACK", "timestamp": 1763765829.421442}
# {"from": "Client", "to": "Server", "seq": 265, "ack": 265, "flags": "FIN", "timestamp": 1763765829.421655}
# {"from": "Server", "to": "Client", "seq": 106, "ack": 266, "flags": "ACK", "timestamp": 1763765829.4220228}
# {"from": "Server", "to": "Client", "seq": 107, "ack": 266, "flags": "FIN", "timestamp": 1763765829.422194}
# {"from": "Client", "to": "Server", "seq": 266, "ack": 108, "flags": "ACK", "timestamp": 1763765829.422454}


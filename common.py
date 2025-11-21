# common.py
import json
import time

def log_event(logfile, sender, receiver, seq, ack, flags):
    """记录一个 TCP 事件到 JSON 日志"""
    event = {
        "from": sender,
        "to": receiver,
        "seq": seq,
        "ack": ack,
        "flags": flags,
        "timestamp": time.time()
    }
    with open(logfile, "a") as f:
        f.write(json.dumps(event) + "\n")
